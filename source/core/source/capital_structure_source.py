# coding: big5

import csv
import os
from datetime import date
from datetime import datetime
from lxml import html

from . import mops_source
from ..base import date_util

class CapitalStructureSource(mops_source.MopsSource):

    def __init__(self):
        mops_source.MopsSource.__init__(self)
        
        self.URL_ACTIVITY_DATE_TEMPLATE = '''http://mopsov.twse.com.tw/server-java/t05st05?TYPEK=&co_id=%s'''
        self.URL_TEMPLATE = '''http://mopsov.twse.com.tw/server-java/t05st05?TYPEK=&co_id=%s&off=1&step=1&year=%s&month=%s&colorchg=1'''
        self.STOCK_CODE = None
        self.ACTIVITY_DATE_DIR = '../dataset/capital_structure/activity_date/'
        self.HTML_DIR = '../dataset/capital_structure/html/'
        self.CSV_DIR = '../dataset/capital_structure/csv/'
        
        
    def source(self, stock_code, begin_date, end_date):
        self.STOCK_CODE = stock_code
        stock_activity_date_dir = self.get_stock_dir(self.ACTIVITY_DATE_DIR, self.STOCK_CODE)
        stock_html_dir = self.get_stock_dir(self.HTML_DIR, self.STOCK_CODE)
        stock_csv_dir = self.get_stock_dir(self.CSV_DIR, self.STOCK_CODE)
        
        self.init_dates(begin_date, end_date, self.ACTIVITY_DATE_DIR)
        self.source_url_to_html(stock_html_dir)        
        self.source_html_to_csv(stock_html_dir, stock_csv_dir)
        self.source_csv_to_db('capital_structure', stock_csv_dir, self.DB_INSERTION)
   
    def init_dates(self, begin_date, end_date, activity_date_dir):
        self.DATES = []
        
        if not os.path.exists(activity_date_dir):
            os.makedirs(activity_date_dir)

        # Source activity dates from url to html                
        url = self.get_activity_date_url()
        file = self.get_activity_date_filename(activity_date_dir, 'html')
        self.wget(url, file)
        
        # Get activity dates from html
        fd = open(file, 'rb')
        file_content = fd.read()
        fd.close()
        
        content = None
        try:
            content = html.fromstring(file_content.decode('big5-hkscs').replace('&nbsp;', ' '))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            content = html.fromstring(file_content.decode('gb18030').replace('&nbsp;', ' '))
            
        # Step 1. Get all links from html
        from lxml.cssselect import CSSSelector         
        selector = CSSSelector('a')
        found_elements = selector(content)

        # Step 2. Get activity date from links
        YEAR_PATTERN = 'year='
        MONTH_PATTERN = 'month='
        for element in found_elements:
            href = element.get('href')
            if YEAR_PATTERN in href and MONTH_PATTERN in href:
                year_begin_index = href.index(YEAR_PATTERN) + len(YEAR_PATTERN)
                year_end_index = href[year_begin_index:].index('&') + year_begin_index
                year = int(href[year_begin_index:year_end_index])
                month_begin_index = href.index(MONTH_PATTERN) + len(MONTH_PATTERN)
                month_end_index = href[month_begin_index:].index('&') + month_begin_index
                month = int(href[month_begin_index:month_end_index])
                self.DATES.append(date(year, month, 1))
   
    def source_html_to_csv(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in reversed(self.DATES):
            self.source_html_to_csv_single(src_dir, dest_dir, date)

    def source_html_to_csv_single(self, src_dir, dest_dir, date):
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
            content = html.fromstring(src_content.decode('big5-hkscs').replace('&nbsp;', ' ').replace('<BR>', ''))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            content = html.fromstring(src_content.decode('gb18030').replace('&nbsp;', ' ').replace('<BR>', ''))

        found_values = []
        for table in content.xpath('//html/body/center/table[@border="5"]'):
            for items in table.xpath('./tr'):
                for item in items.xpath('./td'):
                    item_values = item.xpath('./font/text()')
                    if item_values:
                        for item_value in item_values:
                            found_value = item_value.replace(' ','').replace('\t','').replace('\n','')
                            found_values.append(found_value)
        
        record = [None] * 17
        record[0] = self.STOCK_CODE
        record[1] = date
        for index, value in enumerate(found_values):
            if value.startswith('是否係申報首次公開發行之輸入'):
                if found_values[index + 1] in ('是'):
                    record[2] = 'Y'
                elif found_values[index + 1] in ('否'):
                    record[2] = 'N'
            elif value.startswith('每股面額'):
                record[3] = self.__get_double(found_values[index + 1])
            elif value.startswith('核定股本股數(股)'):
                record[4] = self.__get_double(found_values[index + 1])
            elif value.startswith('核定股本金額(元)'):
                record[5] = self.__get_double(found_values[index + 1])
            elif value.startswith('實收股本股數(股)'):
                record[6] = self.__get_double(found_values[index + 1])
            elif value.startswith('實收股本金額(元)'):
                record[7] = self.__get_double(found_values[index + 1])
            elif value.startswith('1.創立時資本'):
                record[8] = self.__get_double(found_values[index + 1])
            elif value.startswith('2.現金增資'):
                record[9] = self.__get_double(found_values[index + 1])
            elif value.startswith('3.資本公積轉增資'):   
                record[10] = self.__get_double(found_values[index + 1])
            elif value.startswith('4.盈餘轉增資'):
                record[11] = self.__get_double(found_values[index + 1])
            elif value.startswith('7.合併增資(元)'):
                record[12] = self.__get_double(found_values[index + 1])
            elif value.startswith('8.減資(元)'):
                record[13] = self.__get_double(found_values[index + 1])
            elif value.startswith('11.其他'):
                record[14] = found_values[index + 1]
            elif value.startswith('以現金以外之財產抵充股款者'):
                record[15] = found_values[index + 1]
            elif value.startswith('其他'):
                record[16] = found_values[index + 1]

        csv_writer.writerow(record)
        dest_fd.close()

    def get_activity_date_url(self):
        return self.URL_ACTIVITY_DATE_TEMPLATE % self.STOCK_CODE

    def get_activity_date_filename(self, src_dir, ext):
        return os.path.join(src_dir, self.STOCK_CODE + '.' + ext) 
        
    def get_url(self, date):
        return self.URL_TEMPLATE % (self.STOCK_CODE, date.year, date.month)

    def get_filename(self, src_dir, date, ext):
        return os.path.join(src_dir, date.strftime('%Y-%m') + '.' + ext) 
        
    def __get_double(self, literal):
        literal = literal.replace(',','')
        try:
            return float(literal)
        except ValueError:
            return None
