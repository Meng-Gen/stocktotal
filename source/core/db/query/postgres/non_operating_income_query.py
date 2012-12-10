# coding: big5

from . import query

class NonOperatingIncomeQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    def query_non_operating_income_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, non_operating_income_ratio from
        (
            select activity_date, non_operating_income_ratio, max(report_date) from
            (
                select
                    A.activity_date,
                    A.number / B.number as non_operating_income_ratio,
                    A.report_date
                from IncomeStmt as A
                inner join
                IncomeStmt as B
                on A.stock_code = B.stock_code
                    and A.activity_date = B.activity_date
                    and A.item in ('��~�~���J�X�p', '��~�~���J�ΧQ�q')
                    and B.item in ('�~����~�����|�e�b�Q(�b�l)', '�~����~���|�e�b�Q(�b�l)')
                    and A.report_type = 'C'
                    and B.report_type = 'C'
                    and A.stock_code = ?
            )
            where non_operating_income_ratio is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
