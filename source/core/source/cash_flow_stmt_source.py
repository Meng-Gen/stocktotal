import csv
import logging
import os
import shutil
from datetime import date
from datetime import datetime
from lxml import html

from . import stmt_source
from ..base import logger

class CashFlowStmtSource(stmt_source.StmtSource):

    def __init__(self):
        stmt_source.StmtSource.__init__(self)
        
        self.SOURCE_TYPE = 'cash_flow_stmt'
        self.PROG_TYPE_MAP['individual']['prog_name'] = 't05st36'
        self.PROG_TYPE_MAP['consolidated']['prog_name'] = 't05st39'
        self.ITEM_PREFIXES = {
            'Operating' : [
                '營業活動',
                '│營業活動'
            ],
            'Investing' : [
                '投資活動',
                '│投資活動'
            ],
            'Financing' : [
                '融資活動',
                '│融資活動',
                '理財活動',
                '不影響現金流量之融資活動'
            ],
        }
        self.HTML_DIR = '../dataset/cash_flow_stmt/html/'
        self.TXT_DIR = '../dataset/cash_flow_stmt/txt/'
        self.CSV_DIR = '../dataset/cash_flow_stmt/csv/'

    def source_html_to_csv(self, src_dir, dest_dir, stock_code):
        self.source_html_to_txt(src_dir, self.TXT_DIR, stock_code)
        self.source_txt_to_csv(self.TXT_DIR, dest_dir, stock_code)

    def source_html_to_txt(self, src_dir, dest_dir, stock_code):
        assert os.path.isdir(src_dir)
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)
        for type in self.PROG_TYPE_MAP:
            for date in self.DATES:
                self.source_html_to_txt_single(src_dir, dest_dir, stock_code, type, date)
    
    def source_html_to_txt_single(self, src_dir, dest_dir, stock_code, type, date):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        src_file = self.get_filename(src_stock_dir, type, date, 'html')
        if not os.path.isfile(src_file):
            self.LOGGER.error('''%s doesn't exist''' % src_file)
            return
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        dest_file = self.get_filename(dest_stock_dir, type, date, 'txt')
        self.LOGGER.debug('''%s => %s''' % (src_file, dest_file))
        
        if os.path.getsize(src_file) is 0:
            shutil.copy(src_file, dest_file)
            return
        
        src_file_fd = open(src_file, 'rb')
        content = src_file_fd.read()
        src_file_fd.close()

        table = b''
        try:
            table = html.fromstring(content.decode('utf-8'))
        except UnicodeDecodeError as e:
            self.LOGGER.debug(e)
            table = html.fromstring(content.decode('big5'))

        xpath_stmt = table.xpath('//body/table[@class="hasBorder"]/tr/td/pre/text()')
        if len(xpath_stmt) is 1:
            with open(dest_file, 'w', encoding='utf-8') as fd:
                fd.write(xpath_stmt[0].strip())
            return

        xpath_no_record = table.xpath('//body/center/h3/text()')
        if len(xpath_no_record) is 1:
            with open(dest_file, 'w', encoding='utf-8') as fd:
                fd.write(xpath_no_record[0].strip())
            return
            
    def source_txt_to_csv(self, src_dir, dest_dir, stock_code):
        assert os.path.isdir(src_dir)
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        if not os.path.exists(dest_stock_dir):
            os.makedirs(dest_stock_dir)

        for type in self.PROG_TYPE_MAP:
            for date in self.DATES:
                self.source_txt_to_csv_single(src_dir, dest_dir, stock_code, type, date)

    def source_txt_to_csv_single(self, src_dir, dest_dir, stock_code, type, date):
        src_stock_dir = self.get_stock_dir(src_dir, stock_code)
        src_file = self.get_filename(src_stock_dir, type, date, 'txt')
        if not os.path.isfile(src_file):
            self.LOGGER.error('''%s doesn't exist''' % src_file)
            return
        dest_stock_dir = self.get_stock_dir(dest_dir, stock_code)
        dest_file = self.get_filename(dest_stock_dir, type, date, 'csv')
        self.LOGGER.debug('''%s => %s''' % (src_file, dest_file))

        src_fd = open(src_file, 'rb')
        content = src_fd.read()
        src_fd.close()
        lines = content.decode('utf-8').split('\n')
        
        # No record
        if len(lines) is 1:
            msg = lines[0]
            if msg in self.WHITE_MSG:
                self.LOGGER.info('''%s => %s => No record''' % (src_file, msg))
            else:
                self.LOGGER.error('''%s => %s''' % (src_file, msg))
        # Has record
        else:
            items = self.__fetch_items(lines)
            rows = self.__build_records(items)
            dest_fd = open(dest_file, 'w', newline='')
            csv_writer = csv.writer(dest_fd)
            csv_writer.writerows(rows)
            dest_fd.close()

    def __fetch_items(self, lines):
        items = {
            'Operating' : [],
            'Investing' : [],
            'Financing' : [],
        }
        for line in lines:
            line_strip = line.strip()
            for key in items:
                for prefix in self.ITEM_PREFIXES[key]:
                    if line_strip.startswith(prefix):
                        items[key].append(line)
        for key in items:
            self.LOGGER.debug('''%s: %s''', key, items[key])
        return items

    def __build_records(self, items):
        records = []
        for item in items:
            for line in items[item]:
                words = self.__split_words(line)
                if len(words) > 2:
                    number = self.__get_number(words[1])
                    last_number = self.__get_number(words[2])
                    record = [item, number, last_number]
                    records.append(record)
                    self.LOGGER.info('''record: %s''', record)
        return records        

    def __split_words(self, line):
        words = line.split()
        word_num = len(words)
        for i, word in enumerate(words):
            if (word == '(') or (word == '($'):
                next_i = i + 1
                if next_i < word_num:
                    words[next_i] = '(' + words[next_i]

        fixed_words = []
        for word in words:
            if (word != '') and (word != '(') and (word != '($') and (word != '$'): 
                fixed_words.append(word)
        return fixed_words

    def __get_number(self, number):
        number = number.strip()
        number = number.replace('$', '').replace(',', '')
        if (number[0] == '(') and (number[-1] == ')'):
            number = '-' + number[1:-1]
        return number
        