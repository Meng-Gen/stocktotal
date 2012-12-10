import csv
import logging
import os

from ..base import str_util

class TradingSummarySource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.LOGGER = logging.getLogger()
        self.URL_TEMPLATE = '''http://www.twse.com.tw/ch/trading/fund/BFI82U/BFI82U_print.php?begin_date=%s&end_date=&report_type=day&language=ch&save=csv'''
        self.DATES = []
        self.CSV_DIR = '../dataset/trading_summary/csv/'
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()

    def source(self, begin_date, end_date):
        self.init_dates(begin_date, end_date)
        self.source_url_to_csv(self.CSV_DIR)
        self.source_csv_to_db(self.CSV_DIR, self.DB_INSERTION)

    def init_dates(self, begin_date, end_date):
        from datetime import date
        from datetime import datetime
        from datetime import timedelta

        self.DATES = []
        begin = datetime.strptime(begin_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        self.DATES = [begin + timedelta(n) for n in range(int((end - begin).days + 1))]
            
    def source_url_to_csv(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for date in self.DATES:
            url = self.URL_TEMPLATE % date.strftime('%Y%m%d')
            dest_file = self.get_filename(dest_dir, date)
            self.__wget(url, dest_file)

    def source_csv_to_db(self, src_dir, db_insertion):
        assert os.path.isdir(src_dir)
        for date in self.DATES:
            self.source_csv_to_db_single(src_dir, db_insertion, date)
            
    def source_csv_to_db_single(self, src_dir, db_insertion, date):
        src_file = self.get_filename(src_dir, date)
        assert os.path.isfile(src_file)
        
        self.LOGGER.debug('''{src_file} => db'''.format(src_file=src_file))
        
        csv_reader = csv.reader(open(src_file, 'r'))
        rows = [_ for _ in csv_reader]
        if len(rows) is 1:
            self.LOGGER.info('''{src_file} => No record'''.format(src_file=src_file))
            return
        elif len(rows) is not 6:
            self.LOGGER.info('''{src_file} => Error'''.format(src_file=src_file))
            return

        db_insertion.open()
        for n in range(2, 6):
            r = self.__build_db_record(src_file, rows[n])
            db_insertion.insert_trading_summary(r)
            self.LOGGER.debug(r)
        db_insertion.close()
        
    def get_filename(self, src_dir, date):
        return os.path.join(src_dir, date.strftime('%Y-%m-%d'))
        
    def __wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)

    def __build_db_record(self, src_file, row):
        trading_date = os.path.basename(src_file)
        item = row[0]
        buy = row[1].replace(',','')
        sell = row[2].replace(',','')
        diff = row[3].replace(',','')
        assert str_util.is_float(buy)
        assert str_util.is_float(sell)
        assert str_util.is_float(diff)
        return [trading_date, item, buy, sell, diff]