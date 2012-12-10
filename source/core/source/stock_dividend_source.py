import csv
import os
from lxml import html

from . import standardchartered_source

class StockDividendSource(standardchartered_source.StandardcharteredSource):

    def __init__(self):
        standardchartered_source.StandardcharteredSource.__init__(self)

        self.URL_TEMPLATE = '''http://estockweb.standardchartered.com.tw/z/zc/zcc/zcc_%s.djhtm'''
        self.SOURCE_TYPE = 'stock_dividend'
        self.HTML_DIR = '../dataset/stock_dividend/html/'
        self.CSV_DIR = '../dataset/stock_dividend/csv/'

    def source_html_to_csv(self, src_dir, dest_dir):
        assert os.path.isdir(src_dir)
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        src_file = self.get_filename(src_dir, 'html')
        dest_file = self.get_filename(dest_dir, 'csv')
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

        for table in content.xpath('//html/body/div/table/tr/td[@width="99%"]/table/tr/td/table/tr/td/table'):
            for yearly_dataset in table.xpath('./tr'):
                yearly_data = yearly_dataset.xpath('./td/text()')
                if len(yearly_data) is 7:
                    activity_date = self.get_date(yearly_data[0])
                    if not activity_date:
                        continue
                    record = [
                        self.STOCK_CODE, 
                        activity_date, 
                        self.get_double(yearly_data[1]),
                        self.get_double(yearly_data[2]),
                        self.get_double(yearly_data[3]),
                        self.get_double(yearly_data[4]),
                        self.get_double(yearly_data[5]),
                        self.get_double(yearly_data[6]),
                    ]
                    csv_writer.writerow(record)
        dest_fd.close()
