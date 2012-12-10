from . import query

class OperatingIncomeQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)
   
    def query(self, stock_code):
        SQL_SELECT = \
        '''
        SELECT A.activity_date, A.income from
        (
            SELECT activity_date, income, max(report_date) FROM OperatingIncome where stock_code = ?
            group by activity_date, income
            order by activity_date
        )
        as A
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_accumlated(self, stock_code):
        SQL_SELECT = \
        '''
            select A.activity_date, A.income, sum(B.income) from
            (
                select max(report_date), activity_date, income from OperatingIncome
                where stock_code = ?
                group by activity_date
            ) as A,
            (
                select max(report_date), activity_date, income from OperatingIncome
                where stock_code = ?
                group by activity_date
            ) as B
            where B.activity_date <= A.activity_date
            and strftime('%Y', B.activity_date) = strftime('%Y', A.activity_date)
            group by A.activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code])
        
    def query_yoy(self, stock_code):
        SQL_SELECT = \
        '''
            select date, YoY from
            (
                select
                    B.activity_date as date,
                    B.income / A.income - 1 as YoY,
                    max(B.report_date)
                from OperatingIncome as A
                inner join
                OperatingIncome as B
                on A.stock_code = B.stock_code
                    and strftime('%Y', B.activity_date) - strftime('%Y', A.activity_date) = 1
                    and strftime('%m-%d', B.activity_date) = strftime('%m-%d', A.activity_date)
                    and A.stock_code = ?
                group by B.activity_date
            )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])        
        
    def query_accumlated_yoy(self, stock_code):
        SQL_SELECT = \
        '''
            select
                D.date,
                D.accumlated / C.accumlated - 1 as YoY
            from
            (
                select A.activity_date as date, sum(B.income) as accumlated from
                (
                    select max(report_date), activity_date, income from OperatingIncome
                    where stock_code = ?
                    group by activity_date
                ) as A,
                (
                    select max(report_date), activity_date, income from OperatingIncome
                    where stock_code = ?
                    group by activity_date
                ) as B
                where B.activity_date <= A.activity_date
                and strftime('%Y', B.activity_date) = strftime('%Y', A.activity_date)
                group by A.activity_date
            ) as C
            inner join
            (
                select A.activity_date as date, sum(B.income) as accumlated from
                (
                    select max(report_date), activity_date, income from OperatingIncome
                    where stock_code = ?
                    group by activity_date
                ) as A,
                (
                    select max(report_date), activity_date, income from OperatingIncome
                    where stock_code = ?
                    group by activity_date
                ) as B
                where B.activity_date <= A.activity_date
                and strftime('%Y', B.activity_date) = strftime('%Y', A.activity_date)
                group by A.activity_date
            ) as D
            on strftime('%Y', D.date) - strftime('%Y', C.date) = 1
            and strftime('%m-%d', D.date) = strftime('%m-%d', C.date)
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code, stock_code]) 
        