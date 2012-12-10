from . import stmt_source

class BalanceSheetSource(stmt_source.StmtSource):

    def __init__(self):
        stmt_source.StmtSource.__init__(self)
        
        self.SOURCE_TYPE = 'balance_sheet'
        self.PROG_TYPE_MAP['individual']['prog_name'] = 't05st31'
        self.PROG_TYPE_MAP['consolidated']['prog_name'] = 't05st33'
        self.HTML_DIR = '../dataset/balance_sheet/html/'
        self.CSV_DIR = '../dataset/balance_sheet/csv/'
