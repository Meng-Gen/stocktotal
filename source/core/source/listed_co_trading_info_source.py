# coding: utf8

import csv
import os
from datetime import date
from datetime import datetime
from lxml import html

from . import twse_source

class ListedCoTradingInfoSource(twse_source.TwseSource):

    def __init__(self):
        twse_source.TwseSource.__init__(self)
        self.URL_TEMPLATE = '''http://www.twse.com.tw/ch/trading/exchange/FMSRFK/genpage/Report%s12/%s_F3_1_10_%s.php?STK_NO=%s&myear=%s'''
        self.HTML_DIR = '../dataset/listed_co_trading_info/html/'
        self.CSV_DIR = '../dataset/listed_co_trading_info/csv/'

    def source(self, stock_code, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_html(self.HTML_DIR, stock_code)
        self.source_csv_to_db('listed_co_trading_info', self.CSV_DIR, self.DB_INSERTION, stock_code)

    def source_bypass_url(self, stock_code, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR, stock_code)
        self.source_csv_to_db('listed_co_trading_info', self.CSV_DIR, self.DB_INSERTION, stock_code)
        
    def init_dates(self, begin_date, end_date):
        self.DATES = []
        begin = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        for yearly in range(begin.year, end.year + 1):
            self.DATES.append(date(yearly, 1, 1))
        
    def source_url_to_html(self, dest_dir, stock_code):
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)
        for single_date in self.DATES:
            self.source_url_to_html_single(dest_dir, stock_code, single_date)

    def source_url_to_html_single(self, dest_dir, stock_code, single_date):
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        url = self.get_url(stock_code, single_date)
        dest_file = self.get_filename(dest_stock_dir, single_date, 'html')
        self.wget(url, dest_file)
        self.__avoid_blocking()
        
    def source_html_to_csv(self, src_dir, dest_dir, stock_code):
        if not os.path.isdir(src_dir):
            self.LOGGER.error('''%s doesn't exist''' % src_dir)
            return
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)
        for single_date in self.DATES:
            self.source_html_to_csv_single(src_dir, dest_dir, stock_code, single_date)

    def source_html_to_csv_single(self, src_dir, dest_dir, stock_code, single_date):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        src_file = self.get_filename(src_stock_dir, single_date, 'html')
        if not os.path.isfile(src_file):
            self.LOGGER.error('''%s doesn't exist''' % src_file)
            return
        src_fd = open(src_file, 'rb')
        file_content = src_fd.read()
        src_fd.close()
        if file_content == b'':
            self.LOGGER.error('''%s zero file size''' % src_file)
            return        
        content = None       
        try:
            content = html.fromstring(file_content.decode('big5-hkscs').replace('&nbsp;', ' '))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            content = html.fromstring(file_content.decode('gb18030').replace('&nbsp;', ' '))
        
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        dest_file = self.get_filename(dest_stock_dir, single_date, 'csv')
        self.LOGGER.debug('''%s => %s''' % (src_file, dest_file))
        dest_fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(dest_fd)
        for content_block in content.xpath('//html/body/table/tr[@id="contentblock"]/td/table[@id="contentHeader"]/tr'):
            for board in content_block.xpath('./td/form/table[@class="board_trad"]'):
                for item_block in board.xpath('./tr[@class="basic2"]'):
                    activity_date_block = item_block.xpath('./td/div/text()')
                    if len(activity_date_block) is not 2:
                        continue
                    items = item_block.xpath('./td/text()')
                    assert len(items) is 9
                    
                    year = int(activity_date_block[0]) + 1911
                    month = int(activity_date_block[1])
                    csv_record = [
                        stock_code, 
                        date(year, month, 1),
                        self.__fix_number(items[2]),
                        self.__fix_number(items[3]),
                        self.__fix_number(items[4]), 
                        self.__fix_number(items[5]), 
                        self.__fix_number(items[6]),
                        self.__fix_number(items[7]),
                        self.__fix_number(items[8]),
                    ]
                    csv_writer.writerow(csv_record) 
        dest_fd.close()           
                
    def source_csv_to_db(self, source_type, src_dir, db_insertion, stock_code):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        assert os.path.isdir(src_stock_dir)
        for single_date in self.DATES:
            self.source_csv_to_db_single(source_type, src_stock_dir, db_insertion, single_date)
        
    def get_stock_dir(self, src_dir, stock_code):
        return os.path.join(src_dir, stock_code)

    def get_url(self, stock_code, date):
        year = date.year
        return self.URL_TEMPLATE % (year, year, stock_code, stock_code, year)
       
    def get_filename(self, src_dir, date, ext):
        return os.path.join(src_dir, '''%s.%s''' % (date.strftime('%Y'), ext))        
        
    def __avoid_blocking(self):
        import time
        time.sleep(3)

    def __fix_number(self, number):
        return number.strip().replace(',','')