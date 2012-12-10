# coding: big5

from . import query

class EvaluationIndicatorQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

        self.SQL_SELECT_GROWTH_RATE = \
        '''
        select A.activity_date, A.number / avg(B.number) - 1 as number
        from 
            ({item}) as A,
            ({item}) as B
        where strftime('%m-%d', A.activity_date) = strftime('%m-%d', B.activity_date)
        and strftime('%Y', A.activity_date) - strftime('%Y', B.activity_date) in (1, 2)
        group by A.activity_date
        '''

    def query_inventory_index(self, stock_code):
        SQL_SELECT = self.SQL_SELECT_DIFFERENCE.format(
            minuend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_INVENTORY
            ),
            subtrahend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_REVENUE
            )
        )
        print(SQL_SELECT)
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code])

    def query_receivable_index(self, stock_code):
        SQL_SELECT = self.SQL_SELECT_DIFFERENCE.format(
            minuend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_RECEIVABLES
            ),
            subtrahend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_REVENUE
            )
        )
        print(SQL_SELECT)
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code])

    def query_gross_profit_index(self, stock_code):
        SQL_SELECT = self.SQL_SELECT_DIFFERENCE.format(
            minuend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_REVENUE
            ),
            subtrahend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_GROSS_PROFIT
            )
        )
        print(SQL_SELECT)
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code])
        
    def query_sga_index(self, stock_code):
        SQL_SELECT = self.SQL_SELECT_DIFFERENCE.format(
            minuend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_SGA
            ),
            subtrahend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_REVENUE
            )
        )
        print(SQL_SELECT)
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code])
        
    def query_payable_index(self, stock_code):
        SQL_SELECT = self.SQL_SELECT_DIFFERENCE.format(
            minuend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_PAYABLES
            ),
            subtrahend = self.SQL_SELECT_GROWTH_RATE.format(
                item = self.SQL_SELECT_REVENUE
            )
        )
        print(SQL_SELECT)
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code])
