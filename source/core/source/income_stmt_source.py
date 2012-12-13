# coding: utf-8

from . import stmt_source

class IncomeStmtSource(stmt_source.StmtSource):

    def __init__(self):
        stmt_source.StmtSource.__init__(self)
        
        self.SOURCE_TYPE = 'income_stmt'
        self.PROG_TYPE_MAP['individual']['prog_name'] = 't05st32'
        self.PROG_TYPE_MAP['consolidated']['prog_name'] = 't05st34'
        self.HTML_DIR = '../dataset/income_stmt/html/'
        self.CSV_DIR = '../dataset/income_stmt/csv/'
