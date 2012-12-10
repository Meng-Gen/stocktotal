# coding: big5

import csv
import os
import xlrd
from datetime import date
from datetime import datetime

from . import twse_source
from ..base import str_util

class ListedCoStatSource(twse_source.TwseSource):

    def __init__(self):
        twse_source.TwseSource.__init__(self)
        
        self.URL_TEMPLATE = '''http://www.twse.com.tw/ch/inc/download.php?l1=Listed+Companies+Monthly+Statistics&l2=P%%2FE+Ratio+%%26+Yield+of+Listed+Stocks&url=/ch/statistics/download/04/001/%s_C04001.zip'''
        self.ZIP_DIR = '../dataset/listed_co_stat/zip/'
        self.XLS_DIR = '../dataset/listed_co_stat/xls/'
        self.CSV_DIR = '../dataset/listed_co_stat/csv/'

    def source(self, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_zip(self.ZIP_DIR)
        self.source_zip_to_xls(self.ZIP_DIR, self.XLS_DIR)
        self.source_xls_to_csv(self.XLS_DIR, self.CSV_DIR)
        self.source_csv_to_db('listed_co_stat', self.CSV_DIR, self.DB_INSERTION)
    
    def source_xls_to_csv(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in reversed(self.DATES):
            self.source_xls_to_csv_single(src_dir, dest_dir, date)    

    # CSV fields should contains: Report Date, Stock's Code, Latest Price, PER, Yield, PBR	
    def source_xls_to_csv_single(self, src_dir, dest_dir, date):
        self.__source_v3_xls_to_csv_single(src_dir, dest_dir, date)
        self.__source_v2_xls_to_csv_single(src_dir, dest_dir, date)
        self.__source_v1_xls_to_csv_single(src_dir, dest_dir, date)

    def get_url(self, date):
        return self.URL_TEMPLATE % date.strftime('%Y%m')
        
    def get_filename(self, src_dir, date, ext):
        return os.path.join(src_dir, date.strftime('%Y-%m') + '.' + ext)
        
    def __source_v3_xls_to_csv_single(self, src_dir, dest_dir, date):
        src_file = self.get_filename(src_dir, date, 'xls')
        assert os.path.isfile(src_file)
        
        if date < datetime(2007, 4, 1).date():
            return
        
        book = xlrd.open_workbook(src_file)
        sheet = book.sheet_by_index(0)
        assert sheet.ncols is 10
        assert sheet.cell(4, 0).value.strip() == 'Code & Name'
        assert sheet.cell(4, 8).value.strip() in ('PBR', 'ＰＢＲ')
        
        dest_file = self.get_filename(dest_dir, date, 'csv')
        fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(fd)
        for r in self.__build_sheet_records(sheet, 0, 5):
            r = [date.strftime('%Y-%m-%d')] + r
            assert len(r) is 6
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        fd.close()
        
    def __source_v2_xls_to_csv_single(self, src_dir, dest_dir, date):
        src_file = self.get_filename(src_dir, date, 'xls')
        assert os.path.isfile(src_file)
    
        if date >= datetime(2007, 4, 1).date() or date < datetime(2000, 9, 1).date():
            return
               
        book = xlrd.open_workbook(src_file)
        sheet = book.sheet_by_index(0)
        assert sheet.ncols is 21
        assert sheet.cell(4, 0).value.strip() in ('Code & Name', 'CODE & NAME')
        assert sheet.cell(4, 11).value.strip() in ('Code & Name', 'CODE & NAME')
        assert sheet.cell(4, 8).value.strip() in ('PBR', 'ＰＢＲ')
        assert sheet.cell(4, 19).value.strip() in ('PBR', 'ＰＢＲ')
        
        dest_file = self.get_filename(dest_dir, date, 'csv')
        fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(fd)
        for r in self.__build_sheet_records(sheet, 0, 5):
            r = [date.strftime('%Y-%m-%d')] + r
            assert len(r) is 6
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        for r in self.__build_sheet_records(sheet, 11, 5):
            r = [date.strftime('%Y-%m-%d')] + r
            assert len(r) is 6
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        fd.close()
        
    def __source_v1_xls_to_csv_single(self, src_dir, dest_dir, date):
        src_file = self.get_filename(src_dir, date, 'xls')
        assert os.path.isfile(src_file)
    
        if date >= datetime(2000, 9, 1).date():
            return

        book = xlrd.open_workbook(src_file)
        sheet = book.sheet_by_index(0)
        if date == datetime(2000, 5, 1).date():
            header_last_row = 5
        elif date <= datetime(1999, 7, 1).date():
            header_last_row = 8
        else:
            header_last_row = 4
        
        assert sheet.ncols in (17, 11)
        assert sheet.cell(header_last_row, 0).value.strip() in ('Code & Name', 'CODE & NAME')
        assert sheet.cell(header_last_row, 6).value.strip() in ('Code & Name', 'CODE & NAME')
        assert sheet.cell(header_last_row, 4).value.strip() in ('PBR', 'ＰＢＲ')
        assert sheet.cell(header_last_row, 10).value.strip() in ('PBR', 'ＰＢＲ')

        dest_file = self.get_filename(dest_dir, date, 'csv')
        fd = open(dest_file, 'w', newline='')
        csv_writer = csv.writer(fd)
        begin_row = header_last_row + 1
        for r in self.__build_bad_sheet_records(sheet, 0, begin_row):
            r = [date.strftime('%Y-%m-%d')] + r
            assert len(r) is 6
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        for r in self.__build_bad_sheet_records(sheet, 6, begin_row):
            r = [date.strftime('%Y-%m-%d')] + r
            assert len(r) is 6
            csv_writer.writerow(r)  
            self.LOGGER.debug('''%s => %s''' % (r, dest_file))
        fd.close()
        
    def __build_sheet_records(self, sheet, begin_col, begin_row):
        for curr_row in range(begin_row, sheet.nrows):
            r = sheet.row_values(curr_row)
            first_cell = r[begin_col]
        
            if r[begin_col] == '':
                continue
            if r[begin_col + 3] == '' and r[begin_col + 5] == '' \
                    and r[begin_col + 7] == '' and r[begin_col + 9] == '':
                continue
            if isinstance(first_cell, float):
                first_cell = int(first_cell)
            elif isinstance(first_cell, str):
                first_cell = first_cell.replace(' ','')
            yield [first_cell, r[begin_col + 3], r[begin_col + 5], r[begin_col + 7], r[begin_col + 9]]

    def __build_bad_sheet_records(self, sheet, begin_col, begin_row):
        for curr_row in range(begin_row, sheet.nrows):
            r = sheet.row_values(curr_row)
            stock_code = self.__fix_stock_code(r[begin_col])
            latest_price = self.__fix_real_number(r[begin_col + 1])
            per = self.__fix_real_number(r[begin_col + 2])
            dividend_yield = self.__fix_real_number(r[begin_col + 3])
            pbr = self.__fix_real_number(r[begin_col + 4])

            if stock_code == '':
                continue
            if latest_price == '' and per == '' and dividend_yield == '' and pbr == '':
                continue
            yield [stock_code, latest_price, per, dividend_yield, pbr]
    
    def __fix_stock_code(self, bad_stock_code):
        space_removed = bad_stock_code.replace(' ','')
        stock_code = space_removed[0:4]
        # Quickly get possible stock_code
        if stock_code.isdigit(): 
            return stock_code
        return space_removed

    def __fix_real_number(self, bad_str):
        if str_util.is_float(bad_str):
            return float(bad_str)
        assert str_util.is_str(bad_str)
        splitted = bad_str.split()
        for test_str in splitted:
            if str_util.is_float(test_str):
                return float(test_str)
        return ''