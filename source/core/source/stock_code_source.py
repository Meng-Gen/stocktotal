import csv
import os

class StockCodeSource():

    def __init__(self):
        from ..db.insertion import insertion_factory
        
        self.URLS = {
            'LISTED': 'http://brk.tse.com.tw:8000/isin/C_public.jsp?strMode=2',
            'OTC': 'http://brk.tse.com.tw:8000/isin/C_public.jsp?strMode=4',
        }
        self.LOCAL_DIR = '../dataset/stock_code/local/'
        self.CSV_DIR = '../dataset/stock_code/csv/'
        self.DB_INSERTION = insertion_factory.InsertionFactory().insertion()
   
    def source(self):
        self.source_url_to_local(self.LOCAL_DIR)
        self.source_local_to_csv_batch(self.LOCAL_DIR, self.CSV_DIR)
        self.source_csv_to_db_batch(self.CSV_DIR, self.DB_INSERTION)
    
    def source_url_to_local(self, dest_dir):
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)       
        self.__wget(self.URLS['LISTED'], os.path.join(self.LOCAL_DIR, 'listed_company.html'))
        self.__wget(self.URLS['OTC'], os.path.join(self.LOCAL_DIR, 'otc_company.html'))

    def source_local_to_csv_batch(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        for file in os.listdir(src_dir):
            src_file = os.path.join(src_dir, file)
            file_name, file_ext = os.path.splitext(file)
            dest_file = os.path.join(dest_dir, file + '.csv')
            self.source_local_to_csv(src_file, dest_file)
        
    def source_local_to_csv(self, src_file, dest_file):
        from lxml import html

        assert os.path.isfile(src_file)

        src_file_h = open(src_file)
        content = src_file_h.read()
        src_file_h.close()

        csv_writer = csv.writer(open(dest_file, 'w', newline=''))
        table = html.fromstring(content)
        for row in table.xpath('//body/table[@class="h4"]/tr'):
            columns = [_.strip() for _ in row.xpath('./td/text()')]
            if len(columns) is 5:
                csv_writer.writerow(columns[0].split() + columns[1:4] + [''] + columns[4:])
            elif len(columns) is 6:
                csv_writer.writerow(columns[0].split() + columns[1:])

    def source_csv_to_db_batch(self, src_dir, db_insertion):
        assert os.path.isdir(src_dir)
        for file in os.listdir(src_dir):
            self.source_csv_to_db(os.path.join(src_dir, file), db_insertion)

    def source_csv_to_db(self, src_file, db_insertion):
        assert os.path.isfile(src_file)

        db_insertion.open()
        csv_reader = csv.reader(open(src_file, "r"))
        for r in csv_reader:
            db_insertion.insert_stock_code(r)
        db_insertion.close()

    def __wget(self, url, dest_file):
        from ..base import wget
        cmdline = '''\"{url}\" --waitretry=3 -O \"{dest_file}\"'''.format(url=url, dest_file=dest_file)
        wget.wget(cmdline)
