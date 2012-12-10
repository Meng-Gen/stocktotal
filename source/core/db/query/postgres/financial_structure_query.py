# coding: big5

from . import query

class FinancialStructureQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)
    
    def query_equity_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, equity_ratio from
        (
            select activity_date, equity_ratio, max(report_date) from
            (
                select
                E.activity_date,
                E.number / A.number as equity_ratio,
                E.report_date
                from BalanceSheet as E
                inner join
                BalanceSheet as A
                on E.stock_code = A.stock_code
                and E.activity_date = A.activity_date
                and E.item = '股東權益總計'
                and A.item = '資產總計'
                and E.report_type = 'C'
                and A.report_type = 'C'
                and E.stock_code = ?
            )
            where equity_ratio is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_debt_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, debt_ratio from
        (
            select activity_date, debt_ratio, max(report_date) from
            (
                select
                D.activity_date,
                D.number / A.number as debt_ratio,
                D.report_date
                from BalanceSheet as D
                inner join
                BalanceSheet as A
                on D.stock_code = A.stock_code
                and D.activity_date = A.activity_date
                and D.item = '負債總計'
                and A.item = '資產總計'
                and D.report_type = 'C'
                and A.report_type = 'C'
                and D.stock_code = ?
            )
            where debt_ratio is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_equity_multiplier(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, equity_multiplier from
        (
            select activity_date, equity_multiplier, max(report_date) from
            (
                select
                E.activity_date,
                A.number / E.number as equity_multiplier,
                E.report_date
                from BalanceSheet as E
                inner join
                BalanceSheet as A
                on E.stock_code = A.stock_code
                and E.activity_date = A.activity_date
                and E.item = '股東權益總計'
                and A.item = '資產總計'
                and E.report_type = 'C'
                and A.report_type = 'C'
                and E.stock_code = ?
            )
            where equity_multiplier is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
