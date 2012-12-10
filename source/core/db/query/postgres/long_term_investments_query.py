# coding: big5

from . import query

class LongTermInvestmentsQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    def query_long_term_investments_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, long_term_investments_ratio from
        (
            select activity_date, long_term_investments_ratio, max(report_date) from
            (
                select
                L.activity_date,
                L.number / A.number as long_term_investments_ratio,
                L.report_date
                from BalanceSheet as L
                inner join
                BalanceSheet as A
                on L.stock_code = A.stock_code
                and L.activity_date = A.activity_date
                and L.item in ('長期投資合計', '基金及投資')
                and A.item = '資產總計'
                and L.report_type = 'C'
                and A.report_type = 'C'
                and L.stock_code = ?
            )
            where long_term_investments_ratio is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
