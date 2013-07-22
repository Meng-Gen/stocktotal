# coding: utf-8

import csv
import os
import datetime

from . import mops_source
from ..base import date_util

class OperatingIncomeBaseSource(mops_source.MopsSource):

    def __init__(self):
        mops_source.MopsSource.__init__(self)

    def source(self, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_html(self.HTML_DIR)
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR)
        self.source_csv_to_db('operating_income', self.CSV_DIR, self.DB_INSERTION)
   
    def source_html_to_csv(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in reversed(self.DATES):
            self.source_html_to_csv_single(src_dir, dest_dir, date)    

    def source_html_to_csv_single(self, src_dir, dest_dir, date):
        from lxml import html
        
        src_file = self.get_filename(src_dir, date, 'html')
        dest_file = self.get_filename(dest_dir, date, 'csv')
        self.LOGGER.debug('''{src_file} => {dest_file}'''.format(src_file=src_file, dest_file=dest_file))
        assert os.path.isfile(src_file)
        
        dest_fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(dest_fd)
        
        src_fd = open(src_file, 'rb')
        src_content = src_fd.read()
        src_fd.close()

        content = None
        try:
            content = html.fromstring(src_content.decode('big5-hkscs').replace('&nbsp;', ' '))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            content = html.fromstring(src_content.decode('gb18030').replace('&nbsp;', ' '))
            
        for category in content.xpath('//html/body/center/table'):
            for co_list in category.xpath('./tr/td[@colspan="2"]/table'):
                for co in co_list.xpath('./tr[@align="right"]'):
                    # Ignore summary of this category
                    summary = co.xpath('./th/text()')
                    if len(summary) is 1:
                        continue

                    items = co.xpath('./td/text()')
                    stock_code = items[0]

                    this_month_record = [
                        date, 
                        stock_code, 
                        date_util.get_this_month_by(date),
                        items[2].strip().replace(',','')
                    ]
                    csv_writer.writerow(this_month_record)
                    
                    last_month_record = [
                        date, 
                        stock_code, 
                        date_util.get_last_month_by(date),
                        items[3].strip().replace(',','')
                    ]
                    if items[3].strip() == '不適用':
                        self.LOGGER.debug('''Skipped record => {record}'''.format(record=last_month_record))
                    else:
                        csv_writer.writerow(last_month_record)

                    last_year_record = [
                        date, 
                        stock_code, 
                        date_util.get_last_year_by(date),
                        items[4].strip().replace(',','')
                    ]
                    csv_writer.writerow(last_year_record)
        dest_fd.close()
            
    def get_url(self, date):
        return self.URL_TEMPLATE % (date.year - 1911, date.month)
        
    def get_filename(self, src_dir, date, ext):
        return os.path.join(src_dir, date.strftime('%Y-%m') + '.' + ext) 

        

class OperatingIncomeTwSource(OperatingIncomeBaseSource):

    def __init__(self):
        OperatingIncomeBaseSource.__init__(self)
        self.URL_TEMPLATE = '''http://mops.twse.com.tw/t21/sii/t21sc03_%s_%s.html'''
        self.HTML_DIR = '../dataset/operating_income/tw/html/'
        self.CSV_DIR = '../dataset/operating_income/tw/csv/'


        
class OperatingIncomeTwoSource(OperatingIncomeBaseSource):

    def __init__(self):
        OperatingIncomeBaseSource.__init__(self)
        self.URL_TEMPLATE = '''http://mopsov.twse.com.tw/t21/otc/t21sc03_%s_%s.html'''
        self.HTML_DIR = '../dataset/operating_income/two/html/'
        self.CSV_DIR = '../dataset/operating_income/two/csv/'


        
class OperatingIncomeSource():

    def __init__(self):
        pass

    def source(self, begin_date, end_date):
        OperatingIncomeTwSource().source(begin_date, end_date)
        OperatingIncomeTwoSource().source(begin_date, end_date)
