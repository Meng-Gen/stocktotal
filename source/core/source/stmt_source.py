# coding: utf-8

import csv
import logging
import os
from datetime import date
from datetime import datetime
from lxml import html

from ..base import date_util
from ..base import str_util
from ..base import logger

class StmtSource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.LOGGER = logging.getLogger()
        self.SOURCE_TYPE = ''
        self.DATES = []
        self.PROG_TYPE_MAP = {
            'individual' : { 
                'prog_name' : '', 
                'prefix' : 'I',
            },
            'consolidated' : {
                'prog_name' : '', 
                'prefix' : 'C',            
            },
        }
        self.WHITE_MSG = [
            '資料庫中查無需求資料',
            '無應編製合併財報之子公司',
            '外國發行人免申報個別財務報表資訊，請至合併財務報表查詢',
        ]
        self.URL_TEMPLATE = \
            '''http://mops.twse.com.tw/mops/web/ajax_%s?TYPEK=all&TYPEK2=&checkbtn=&co_id=%s&code1=&encodeURIComponent=1&firstin=1&isnew=false&keyword4=&off=1&queryName=co_id&season=%02d&step=1&year=%d'''
        self.HTML_DIR = ''
        self.TXT_DIR = ''
        self.CSV_DIR = ''
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()

    def source(self, stock_code, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_html(self.HTML_DIR, stock_code)
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR, stock_code)
        self.source_csv_to_db(self.SOURCE_TYPE, self.CSV_DIR, self.DB_INSERTION, stock_code)

    def source_bypass_url(self, stock_code, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR, stock_code)
        self.source_csv_to_db(self.SOURCE_TYPE, self.CSV_DIR, self.DB_INSERTION, stock_code)
        
    def init_dates(self, begin_date, end_date):
        self.DATES = []
        begin = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        monthly_begin = 12 * begin.year + begin.month - 1
        monthly_end = 12 * end.year + end.month
        for monthly in range(monthly_begin, monthly_end):
            year, month = divmod(monthly, 12)
            month += 1
            if month in (3, 6, 9, 12):
                self.DATES.append(date(year, month, 1))
        
    def source_url_to_html(self, dest_dir, stock_code):
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)
        for type in self.PROG_TYPE_MAP:
            for date in self.DATES:
                self.source_url_to_html_single(dest_dir, stock_code, type, date)

    def source_url_to_html_single(self, dest_dir, stock_code, type, date):
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        url = self.get_url(type, stock_code, date)
        dest_file = self.get_filename(dest_stock_dir, type, date, 'html')
        self.__wget(url, dest_file)
        self.__avoid_blocking_by_mops()              
        
    def source_html_to_csv(self, src_dir, dest_dir, stock_code):
        if not os.path.isdir(src_dir):
            self.LOGGER.error('''%s doesn't exist''' % src_dir)
            return
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)
        for type in self.PROG_TYPE_MAP:
            for date in self.DATES:
                self.source_html_to_csv_single(src_dir, dest_dir, stock_code, type, date)

    def source_html_to_csv_single(self, src_dir, dest_dir, stock_code, type, date):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        src_file = self.get_filename(src_stock_dir, type, date, 'html')
        if not os.path.isfile(src_file):
            self.LOGGER.error('''%s doesn't exist''' % src_file)
            return
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        dest_file = self.get_filename(dest_stock_dir, type, date, 'csv')
        self.LOGGER.debug('''%s => %s''' % (src_file, dest_file))
    
        src_fd = open(src_file, 'rb')
        content = src_fd.read()
        src_fd.close()

        if content == b'':
            self.LOGGER.error('''%s zero file size''' % src_file)
            return
        
        table = b''
        try:
            table = html.fromstring(content.decode('utf-8').replace('&nbsp;', ' '))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            table = html.fromstring(content.decode('big5').replace('&nbsp;', ' '))
        
        xpath_no_record = table.xpath('//body/center/h3/text()')
        if len(xpath_no_record) is 1:
            with open(dest_file, 'w') as dest_fd:
                dest_fd.write(xpath_no_record[0].strip())
            return

        dest_fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(dest_fd)
        for tr in table.xpath('//tr'):
            tds = tr.xpath('./td/text()')
            if len(tds) is 5:
                item = tds[0].strip().replace(' ','')
                this_number = tds[1].strip().replace(' ','').replace(',', '')
                last_number = tds[3].strip().replace(' ','').replace(',', '')
                csv_record = [item, this_number, last_number]
                csv_writer.writerow(csv_record)            
        dest_fd.close()

    def source_csv_to_db(self, source_type, src_dir, db_insertion, stock_code):
        if not os.path.isdir(src_dir):
            self.LOGGER.error('''{src_dir} doesn't exist'''.format(src_dir=src_dir))
            return

        for type in self.PROG_TYPE_MAP:
            for date in self.DATES:
                self.source_csv_to_db_single(source_type, src_dir, db_insertion, stock_code, type, date)
        
    def source_csv_to_db_single(self, source_type, src_dir, db_insertion, stock_code, type, date):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        src_file = self.get_filename(src_stock_dir, type, date, 'csv')
        if not os.path.isfile(src_file):
            self.LOGGER.error('''{src_file} doesn't exist'''.format(src_file=src_file))
            return
        self.LOGGER.debug('''{src_file} => db'''.format(src_file=src_file))
        
        last_year = date_util.get_last_year_by(date)
        report_type = self.PROG_TYPE_MAP[type]['prefix']
        
        INSERT_SOURCE_TYPE_MAP = {
            'balance_sheet': db_insertion.insert_balance_sheet,
            'income_stmt': db_insertion.insert_income_stmt,
            'cash_flow_stmt': db_insertion.insert_cash_flow_stmt,
        }     
        
        db_insertion.open()
        csv_reader = csv.reader(open(src_file, 'r'))
        for row in csv_reader:
            if len(row) is 1:
                msg = row[0]
                if msg in self.WHITE_MSG:
                    self.LOGGER.info('''{src_file} => {msg} => No record'''.format(src_file=src_file, msg=msg))
                else:
                    self.LOGGER.error('''{src_file} => {msg}'''.format(src_file=src_file, msg=msg))
            elif len(row) in (2, 3):
                number = row[1].replace(',', '')
                if str_util.is_float(number):
                    r = (stock_code, report_type, date, date, row[0], number)
                    INSERT_SOURCE_TYPE_MAP[source_type](r)
            if len(row) is 3:
                number = row[2].replace(',', '')
                if str_util.is_float(number):
                    r = (stock_code, report_type, date, last_year, row[0], number)
                    INSERT_SOURCE_TYPE_MAP[source_type](r)
        db_insertion.close()
        
    def get_stock_dir(self, src_dir, stock_code):
        return os.path.join(src_dir, stock_code)

    def get_url(self, type, stock_code, date):
        prog_name = self.PROG_TYPE_MAP[type]['prog_name']
        quarter = int((date.month + 2)/3)
        chinese_year = date.year - 1911
        return self.URL_TEMPLATE % (prog_name, stock_code, quarter, chinese_year)
       
    def get_filename(self, src_dir, type, date, ext):
        prefix = self.PROG_TYPE_MAP[type]['prefix']
        return os.path.join(src_dir, '''%s_%s.%s''' % (prefix, date.strftime('%Y-%m'), ext))        
        
    def __wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)    
        
    def __avoid_blocking_by_mops(self):
        import time
        time.sleep(3)
                