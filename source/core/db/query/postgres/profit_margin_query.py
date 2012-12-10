# coding: big5

from . import query

class ProfitMarginQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    def query_gross_profit_margin(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, gross_profit_margin from
        (
            select activity_date, gross_profit_margin, max(report_date) from
            (
                select
                A.activity_date,
                A.number / B.number as gross_profit_margin,
                A.report_date
                from IncomeStmt as A
                inner join
                IncomeStmt as B
                on A.stock_code = B.stock_code
                and A.activity_date = B.activity_date
                and A.item = '��~��Q(��l)'
                and B.item = '��~���J�X�p'
                and B.report_type = 'C'
                and B.report_type = 'C'
                and B.stock_code = ?
            )
            where gross_profit_margin is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_operating_profit_margin(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, operating_profit_margin from
        (
            select activity_date, operating_profit_margin, max(report_date) from
            (
                select
                A.activity_date,
                A.number / B.number as operating_profit_margin,
                A.report_date
                from IncomeStmt as A
                inner join
                IncomeStmt as B
                on A.stock_code = B.stock_code
                and A.activity_date = B.activity_date
                and A.item = '��~�b�Q(�b�l)'
                and B.item = '��~���J�X�p'
                and B.report_type = 'C'
                and B.report_type = 'C'
                and B.stock_code = ?
            )
            where operating_profit_margin is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_net_profit_margin(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, net_profit_margin from
        (
            select activity_date, net_profit_margin, max(report_date) from
            (
                select
                I.activity_date,
                I.number / O.number as net_profit_margin,
                I.report_date
                from IncomeStmt as I
                inner join
                IncomeStmt as O
                on I.stock_code = O.stock_code
                and I.activity_date = O.activity_date
                and I.item = '�X���`�l�q'
                and O.item = '��~���J�X�p'
                and I.report_type = 'C'
                and O.report_type = 'C'
                and I.stock_code = ?
            )
            where net_profit_margin is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
