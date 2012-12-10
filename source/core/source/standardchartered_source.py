import csv
import logging
import os
from datetime import date

class StandardcharteredSource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.LOGGER = logging.getLogger()        
        self.URL_TEMPLATE = ''
        self.STOCK_CODE = None
        self.SOURCE_TYPE = None
        self.HTML_DIR = ''
        self.CSV_DIR = ''
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()
        
    def source(self, stock_code):
        self.STOCK_CODE = stock_code
        self.source_url_to_html(self.HTML_DIR)        
        self.source_html_to_csv(self.HTML_DIR, self.CSV_DIR)
        self.source_csv_to_db(self.SOURCE_TYPE, self.CSV_DIR, self.DB_INSERTION)

    def source_url_to_html(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        url = self.__get_url()
        dest_file = self.get_filename(dest_dir, 'html')
        self.__wget(url, dest_file)
        
    def source_html_to_csv(self, src_dir, dest_dir):
        pass

    def source_csv_to_db(self, source_type, src_dir, db_insertion):            
        src_file = self.get_filename(src_dir, 'csv')
        if not os.path.isfile(src_file):
            return    
        self.LOGGER.debug('''{src_file} => db'''.format(src_file=src_file))
        fd = open(src_file, 'r')
        csv_reader = csv.reader(fd)
                
        INSERT_SOURCE_TYPE_MAP = {
            'capital_structure_summary': db_insertion.insert_capital_structure_summary,
            'stock_dividend': db_insertion.insert_stock_dividend,
        }                 
                
        db_insertion.open()
        for r in csv_reader:
            INSERT_SOURCE_TYPE_MAP[source_type](r)
            self.LOGGER.debug(r)
        db_insertion.close()
        
        fd.close()

    def get_filename(self, src_dir, ext):
        return os.path.join(src_dir, self.STOCK_CODE + '.' + ext) 

    # Get date from ROC year to date (Python data type)
    def get_date(self, literal):
        try:
            return date(int(literal) + 1911, 1, 1)
        except ValueError:
            return None        

    def get_double(self, literal):
        literal = literal.replace(',','')    
        try:
            return float(literal)
        except ValueError:
            return None
            
    def __get_url(self):
        return self.URL_TEMPLATE % self.STOCK_CODE

    def __wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)
