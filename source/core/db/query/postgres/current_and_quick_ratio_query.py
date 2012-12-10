# coding: big5

from . import query

class CurrentAndQuickRatioQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)
    
    def query_current_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, current_ratio from
        (
            select activity_date, current_ratio, max(report_date) from
            (
                select
                A.activity_date,
                A.number / B.number as current_ratio,
                A.report_date
                from BalanceSheet as A
                inner join
                BalanceSheet as B
                on A.stock_code = B.stock_code
                and A.activity_date = B.activity_date
                and A.item = '流動資產'
                and B.item = '流動負債'
                and A.report_type = 'C'
                and B.report_type = 'C'
                and A.stock_code = ?
            )
            where current_ratio is not null
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_rapid_ratio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, rapid_ratio from
        (
            select activity_date, rapid_ratio, max(report_date) from
            (
                select
                    C.activity_date,
                    D.rapid / C.number as rapid_ratio,
                    C.report_date
                from BalanceSheet as C,
                (
                    select activity_date, rapid, max(report_date) from
                    (
                        select
                        A.activity_date as activity_date,
                        A.number - B.not_rapid as rapid,
                        A.report_date as report_date
                        from BalanceSheet as A,
                        (
                            select activity_date, not_rapid from
                            (
                                select activity_date, not_rapid, max(report_date) from
                                (
                                    select activity_date, report_date, sum(number) as not_rapid
                                    from BalanceSheet
                                    where report_type = 'C'
                                        and stock_code = ?
                                        and item in ('存 貨', '預付款項', '其他流動資產')
                                    group by activity_date, report_date
                                )
                                group by activity_date
                            )
                        ) as B
                        where A.activity_date = B.activity_date
                        and A.item = '流動資產'
                        and A.report_type = 'C'
                        and A.stock_code = ?
                    )
                    group by activity_date
                    order by activity_date
                ) as D
                where C.activity_date = D.activity_date
                    and C.item = '流動負債'
                    and C.report_type = 'C'
                    and C.stock_code = ?
            )
            group by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code])
