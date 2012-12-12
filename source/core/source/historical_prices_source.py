# coding: utf8

import csv
import logging
import os
from datetime import date
from datetime import datetime
from lxml import html

class HistoricalPricesSource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.LOGGER = logging.getLogger()
        self.URL_TEMPLATE = '''http://finance.yahoo.com/q/hp?s=%s.%s+Historical+Prices'''
        self.URL_DELTA_TEMPLATE = '''http://ichart.finance.yahoo.com/table.csv?s=%s.%s&amp;d=%02d&amp;e=%s&amp;f=%s&amp;g=d&amp;a=%02d&amp;b=%s&amp;c=%s&amp;ignore=.csv'''
        self.HTML_DIR = '../dataset/historical_price/html/'
        self.CSV_DIR = '../dataset/historical_price/csv/'
        self.DELTA_DIR = '../dataset/historical_price/delta/'
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()
    
    def source_tw(self, stock_code):
        self.source(stock_code, 'TW')
       
    def source_two(self, stock_code):
        self.source(stock_code, 'TWO')
    
    def source_delta_tw(self, stock_code, begin_date, end_date):
        self.source_delta(stock_code, 'TW', begin_date, end_date)

    def source_delta_two(self, stock_code, begin_date, end_date):
        self.source_delta(stock_code, 'TWO', begin_date, end_date)
        
    def source(self, stock_code, market_category):
        self.source_url_to_html(self.HTML_DIR, stock_code, market_category)
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR, stock_code)
        self.source_csv_to_db(self.CSV_DIR, self.DB_INSERTION, stock_code)

    def source_delta(self, stock_code, market_category, begin_date, end_date):
        self.source_url_to_csv_delta(self.DELTA_DIR, stock_code, market_category, begin_date, end_date)
        self.source_csv_to_db(self.DELTA_DIR, self.DB_INSERTION, stock_code, market_category)
        
    def source_url_to_html(self, dest_dir, stock_code, market_category):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        url = self.__get_url(stock_code, market_category)
        dest_file = self.__get_filename(dest_dir, stock_code, 'html')
        self.__wget(url, dest_file)

    def source_url_to_csv_delta(self, dest_dir, stock_code, market_category, begin_date, end_date):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        url = self.__get_url_delta(stock_code, market_category, begin_date, end_date)
        dest_file = self.__get_filename(dest_dir, stock_code, 'csv')
        self.__wget(url, dest_file)
        
    def source_html_to_csv(self, src_dir, dest_dir, stock_code):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
    
        src_file = self.__get_filename(src_dir, stock_code, 'html')
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
            
        # Step 1. Get all links from html
        from lxml.cssselect import CSSSelector         
        selector = CSSSelector('a')
        found_elements = selector(content)

        # Step 2. Get CSV links and download CSV
        for element in found_elements:
            href = element.get('href').strip()
            if href.startswith('http://ichart.finance.yahoo.com/table.csv'):
                dest_file = self.__get_filename(dest_dir, stock_code, 'csv')
                self.__wget(href, dest_file)
                break
                
    def source_csv_to_db(self, src_dir, db_insertion, stock_code):
        src_file = self.__get_filename(src_dir, stock_code, 'csv')
        if not os.path.isfile(src_file):
            return
        self.LOGGER.debug('''{src_file} => db'''.format(src_file=src_file))
        with open(src_file, 'r') as fd:
            csv_reader = csv.reader(fd)            
            db_insertion.open()
            for r in csv_reader:
                if r[0] == 'Date':
                    continue
                db_record = [stock_code] + r
                db_insertion.insert_historical_price(db_record)
                self.LOGGER.debug(db_record)
            db_insertion.close()
        
    def __get_stock_dir(self, src_dir, stock_code):
        return os.path.join(src_dir, stock_code)

    def __get_url(self, stock_code, market_category):
        return self.URL_TEMPLATE % (stock_code, market_category)

    def __get_url_delta(self, stock_code, market_category, begin_date, end_date):
        begin = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return self.URL_DELTA_TEMPLATE % (
            stock_code, 
            market_category, 
            end.month - 1, 
            end.day,
            end.year,
            begin.month - 1,
            begin.day,
            begin.year,
        )
        
    def __get_filename(self, src_dir, stock_code, ext):
        return os.path.join(src_dir, '''%s.%s''' % (stock_code, ext))        
        
    def __wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)    
        