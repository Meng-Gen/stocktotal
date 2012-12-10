# coding: big5

import csv
import os
import xlrd
from datetime import date
from datetime import datetime

from . import twse_source

class MarketStatSource(twse_source.TwseSource):

    def __init__(self):
        twse_source.TwseSource.__init__(self)
    
        self.URL_TEMPLATE = '''http://www.twse.com.tw/ch/inc/download.php?l1=Securities+Trading+Monthly+Statistics&l2=Statistics+of+Securities+Market&url=/ch/statistics/download/02/001/%s_C02001.zip'''
        self.ZIP_DIR = '../dataset/market_stat/zip/'
        self.XLS_DIR = '../dataset/market_stat/xls/'
        self.CSV_DIR = '../dataset/market_stat/csv/'

    def source(self, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_zip(self.ZIP_DIR)
        self.source_zip_to_xls(self.ZIP_DIR, self.XLS_DIR)
        self.source_xls_to_csv(self.XLS_DIR, self.CSV_DIR)
        self.source_csv_to_db('market_stat', self.CSV_DIR, self.DB_INSERTION)
    
    def source_xls_to_csv(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in reversed(self.DATES):
            self.source_xls_to_csv_single(src_dir, dest_dir, date)

    def source_xls_to_csv_single(self, src_dir, dest_dir, date):
        self.__source_v2_xls_to_csv_single(src_dir, dest_dir, date)
        self.__source_v1_xls_to_csv_single(src_dir, dest_dir, date)

    def get_url(self, date):
        return self.URL_TEMPLATE % date.strftime('%Y%m')
        
    def get_filename(self, src_dir, date, ext):
        return os.path.join(src_dir, date.strftime('%Y-%m') + '.' + ext)        
        
    def __source_v2_xls_to_csv_single(self, src_dir, dest_dir, date):
        src_file = self.get_filename(src_dir, date, 'xls')
        if not os.path.isfile(src_file):
            return 

        if date < datetime(2003, 6, 1).date():
            return
        book = xlrd.open_workbook(src_file)
        sheet = book.sheet_by_index(0)
        assert sheet.ncols is 15
        assert sheet.cell(12, 14).value == 'Days'
        assert sheet.cell(12, 0).value.strip() == 'Month'
        
        dest_file = self.get_filename(dest_dir, date, 'csv')
        fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(fd)
        for r in self.__build_sheet_records(sheet, 13):
            r = [date.strftime('%Y-%m-%d')] + r
            r = self.__remove_comment_mark(r)
            assert len(r) is 17
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        fd.close()
                
    def __source_v1_xls_to_csv_single(self, src_dir, dest_dir, date):
        src_file = self.get_filename(src_dir, date, 'xls')
        if not os.path.isfile(src_file):
            return 
        
        if date >= datetime(2003, 6, 1).date() or date <= datetime(2000, 9, 1).date():
            return
        book = xlrd.open_workbook(src_file)
        main_sheet = book.sheet_by_index(0)
        assert main_sheet.ncols is 12
        
        if date > datetime(2001, 6, 1).date():
            assert main_sheet.cell(12, 0).value.strip() == 'Month'
        elif date > datetime(2000, 9, 1).date():
            assert main_sheet.cell(11, 0).value.strip() == 'Month'
            assert main_sheet.cell(12, 0).value.strip() == ''
        main_records = self.__build_sheet_records(main_sheet, 13)
        
        rest_sheet = book.sheet_by_index(1)
        assert rest_sheet.ncols is 13
        assert rest_sheet.cell(10, 0).value.strip() == 'Month'
        rest_records = self.__build_sheet_records(rest_sheet, 11)

        assert len(main_records) == len(rest_records)
        
        dest_file = self.get_filename(dest_dir, date, 'csv')
        fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(fd)
        for i in range(len(main_records)):
            assert len(main_records[i]) is 13
            assert len(rest_records[i]) is 14
            assert main_records[i][0] == rest_records[i][0]
            assert main_records[i][1] == rest_records[i][1]
            r = [date.strftime('%Y-%m-%d')] + \
                    main_records[i][:-2] + rest_records[i][2:6] + rest_records[i][-2:-1]
            r = self.__remove_comment_mark(r)
            assert len(r) is 17
            csv_writer.writerow(r)
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        fd.close()
        
    def __build_sheet_records(self, sheet, begin_row):
        rv = []
        
        monthly_curr_year = ''
        for curr_row in range(begin_row, sheet.nrows):
            r = sheet.row_values(curr_row)
            first_cell = r[0].strip()
            
            # Check footer. 
            if first_cell.startswith('註'): 
                break
                
            # Ignore this year summary because it is partial.
            if first_cell.endswith(')月'): 
                continue
                
            # Check if yearly record. Example: 93(2004)
            if first_cell.endswith(')'): 
                curr_date = '''%s-01-01''' % first_cell[first_cell.index('(')+1 : -1]
                sheet_record = [curr_date, 'yearly'] + r[1:]
                rv.append(sheet_record)

            # Check if monthly record. Example: 95年  1月
            if first_cell.endswith('月'): 
                curr_month = 0
                if '年' in first_cell:
                    monthly_curr_year = int(first_cell[:first_cell.index('年')]) + 1911
                    curr_month = int(first_cell[first_cell.index('年')+1 : first_cell.index('月')])
                else:
                    curr_month = int(first_cell[:first_cell.index('月')])
                curr_date = '''%s-%02d-01''' % (monthly_curr_year, curr_month)
                sheet_record = [curr_date, 'monthly'] + r[1:]
                rv.append(sheet_record)
        return rv
        
    def __remove_comment_mark(self, csv_record):
        rv = csv_record[:3]
        for i in range(3, len(csv_record)):
            value = csv_record[i]
            try:
                float(value)
                rv.append(value)
            except ValueError:
                fixed_value = value[value.rindex(' ')+ 1 :].replace(',', '')
                float(fixed_value)
                rv.append(fixed_value)
        return rv
