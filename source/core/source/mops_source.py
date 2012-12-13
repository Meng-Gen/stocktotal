# coding: utf-8

import csv
import logging
import os
import shutil
from datetime import date
from datetime import datetime

class MopsSource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.LOGGER = logging.getLogger()
        self.DATES = []
        self.HTML_DIR = ''
        self.XLS_DIR = ''
        self.CSV_DIR = ''
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()

    def init_dates(self, begin_date, end_date):
        self.DATES = []
        begin = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        monthly_begin = 12 * begin.year + begin.month - 1
        monthly_end = 12 * end.year + end.month
        for monthly in range(monthly_begin, monthly_end):
            year, month = divmod(monthly, 12)
            self.DATES.append(date(year, month + 1, 1))
            
    def source_url_to_html(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in self.DATES:
            url = self.get_url(date)
            dest_file = self.get_filename(dest_dir, date, 'html')
            self.wget(url, dest_file)
            self.avoid_blocking_by_mops()

    def source_zip_to_xls(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in self.DATES:
            src_file = self.get_filename(src_dir, date, 'zip')
            dest_file = self.get_filename(dest_dir, date, 'xls')
            self.source_zip_to_xls_single(src_file, dest_dir, dest_file)
    
    def source_zip_to_xls_single(self, src_file, dest_dir, dest_file):
        from ..base import file_archiver
   
        assert os.path.isfile(src_file)
        assert os.path.isdir(dest_dir)

        archiver_output_dir = os.path.join(dest_dir, 'archiver_output_dir')
        file_archiver.extract(src_file, archiver_output_dir)
        if not os.path.exists(archiver_output_dir):
            self.LOGGER.info('''{src_file} => Failure to extract'''.format(src_file=src_file))
            return

        file_list = os.listdir(archiver_output_dir)
        assert len(file_list) is 1
        sevenzip_output_file = os.path.join(archiver_output_dir, file_list[0])
        shutil.copy(sevenzip_output_file, dest_file)  
        shutil.rmtree(archiver_output_dir)
       
    def source_csv_to_db(self, source_type, src_dir, db_insertion):
        assert os.path.isdir(src_dir)
        for date in self.DATES:
            self.source_csv_to_db_single(source_type, src_dir, db_insertion, date)
            
    def source_csv_to_db_single(self, source_type, src_dir, db_insertion, date):            
        src_file = self.get_filename(src_dir, date, 'csv')
        if not os.path.isfile(src_file):
            return    
        self.LOGGER.debug('''{src_file} => db'''.format(src_file=src_file))
        fd = open(src_file, 'r')
        csv_reader = csv.reader(fd)
        
        INSERT_SOURCE_TYPE_MAP = {
            'operating_income': db_insertion.insert_operating_income,
            'capital_structure': db_insertion.insert_capital_structure,
        }        
        
        db_insertion.open()
        for r in csv_reader:
            INSERT_SOURCE_TYPE_MAP[source_type](r)
            self.LOGGER.debug(r)
        db_insertion.close()
        
        fd.close()

    def get_stock_dir(self, src_dir, stock_code):
        return os.path.join(src_dir, stock_code)        
        
    def get_url(self, date):
        pass
        
    def get_filename(self, src_dir, date, ext):
        pass
        
    def wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)

    def avoid_blocking_by_mops(self):
        import time
        time.sleep(3)