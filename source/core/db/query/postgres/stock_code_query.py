# coding: big5

from . import query



class StockCodeQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    def query_listed_co(self):
        sql_cmd = '''select code from StockCode where cfi_code = \'ESVUFR\' and market_category = \'�W��\''''
        return self.exec_query_stock_code(sql_cmd)

    def query_otc(self):
        sql_cmd = '''select code from StockCode where cfi_code = \'ESVUFR\' and market_category = \'�W�d\''''
        return self.exec_query_stock_code(sql_cmd)
       
    def exec_query_stock_code(self, sql_cmd):
        self.open()
        rv = [_[0] for _ in self.DB_CONN.prepare(sql_cmd)]
        self.close()
        return rv
