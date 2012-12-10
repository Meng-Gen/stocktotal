# coding: big5

from . import query

"""
CCC = DIO + DSO - DPO
where 
    DIO = days inventory outstanding
    DSO = days sales outstanding
    DPO = days payable outstanding        
"""
class CccQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)
     
    def query_dio(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, dio from
        (
            select
                C.activity_date,
                C.avg_inventory / D.cogs * 365 as dio
            from
            (
                -- Average Inventory
                select A.activity_date, A.number, avg(B.number) as avg_inventory from
                (
                    select max(report_date), activity_date, number from BalanceSheet
                    where
                        report_type = 'C'
                        and stock_code = ?
                        and item = '存 貨'
                    group by activity_date
                ) as A,
                (
                    select max(report_date), activity_date, number from BalanceSheet
                    where
                        report_type = 'C'
                        and stock_code = ?
                        and item = '存 貨'
                    group by activity_date
                ) as B
                where B.activity_date <= A.activity_date
                and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                group by A.activity_date
            ) as C,
            (
                --COGS
                select
                    max(report_date),
                    activity_date,
                    case
                        when strftime('%m', activity_date) = '03' then number * 4/1
                        when strftime('%m', activity_date) = '06' then number * 4/2
                        when strftime('%m', activity_date) = '09' then number * 4/3
                        else number
                    end as cogs
                from IncomeStmt
                where
                    report_type = 'C'
                    and stock_code = ?
                    and item = '營業成本合計'
                group by activity_date
            ) as D
            where C.activity_date = D.activity_date
        )
        where dio is not null
        order by activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code])

    def query_dso(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, dso from
        (
            select
                C.activity_date,
                C.avg_receivables / D.revenue * 365 as dso
            from
            (
                -- Average Receivables
                select A.activity_date, avg(B.receivables) as avg_receivables from
                (
                    select activity_date, sum(number) as receivables from
                    (
                        select activity_date, item, number, max(report_date) from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item like '%應收帳款%'
                        group by activity_date, item
                    )
                    group by activity_date
                ) as A,
                (
                    select activity_date, sum(number) as receivables from
                    (
                        select activity_date, item, number, max(report_date) from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item like '%應收帳款%'
                        group by activity_date, item
                    )
                    group by activity_date
                ) as B
                where B.activity_date <= A.activity_date
                and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                group by A.activity_date      
            ) as C,
            (
                -- Revenue
                select
                    max(report_date),
                    activity_date,
                    case
                        when strftime('%m', activity_date) = '03' then number * 4/1
                        when strftime('%m', activity_date) = '06' then number * 4/2
                        when strftime('%m', activity_date) = '09' then number * 4/3
                        else number
                    end as revenue
                from IncomeStmt
                where
                    report_type = 'C'
                    and stock_code = ?
                    and item = '營業收入合計'
                group by activity_date
            ) as D
            where C.activity_date = D.activity_date
        )
        where dso is not null
        order by activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code])

    def query_dpo(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, dpo from
        (
            select
                C.activity_date,
                C.avg_payables / D.cogs * 365 as dpo
            from
            (
                -- Average Payables
                select A.activity_date, avg(B.payables) as avg_payables from
                (
                    select activity_date, sum(number) as payables from
                    (
                        select activity_date, item, number, max(report_date) from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item like '%應付帳款%'
                        group by activity_date, item
                    )
                    group by activity_date
                ) as A,
                (
                    select activity_date, sum(number) as payables from
                    (
                        select activity_date, item, number, max(report_date) from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item like '%應付帳款%'
                        group by activity_date, item
                    )
                    group by activity_date
                ) as B
                where B.activity_date <= A.activity_date
                and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                group by A.activity_date      
            ) as C,
            (
                --COGS
                select
                    max(report_date),
                    activity_date,
                    case
                        when strftime('%m', activity_date) = '03' then number * 4/1
                        when strftime('%m', activity_date) = '06' then number * 4/2
                        when strftime('%m', activity_date) = '09' then number * 4/3
                        else number
                    end as cogs
                from IncomeStmt
                where
                    report_type = 'C'
                    and stock_code = ?
                    and item = '營業成本合計'
                group by activity_date
            ) as D
            where C.activity_date = D.activity_date
        )
        where dpo is not null
        order by activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code, stock_code])

    def query_ccc(self, stock_code):
        SQL_SELECT = \
        '''
        select A.activity_date, A.dio + B.dso - C.dpo as ccc from
        (
            select activity_date, dio from
            (
                select
                    C.activity_date,
                    C.avg_inventory / D.cogs * 365 as dio
                from
                (
                    -- Average Inventory
                    select A.activity_date, A.number, avg(B.number) as avg_inventory from
                    (
                        select max(report_date), activity_date, number from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item = '存 貨'
                        group by activity_date
                    ) as A,
                    (
                        select max(report_date), activity_date, number from BalanceSheet
                        where
                            report_type = 'C'
                            and stock_code = ?
                            and item = '存 貨'
                        group by activity_date
                    ) as B
                    where B.activity_date <= A.activity_date
                    and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                    group by A.activity_date
                ) as C,
                (
                    --COGS
                    select
                        max(report_date),
                        activity_date,
                        case
                            when strftime('%m', activity_date) = '03' then number * 4/1
                            when strftime('%m', activity_date) = '06' then number * 4/2
                            when strftime('%m', activity_date) = '09' then number * 4/3
                            else number
                        end as cogs
                    from IncomeStmt
                    where
                        report_type = 'C'
                        and stock_code = ?
                        and item = '營業成本合計'
                    group by activity_date
                ) as D
                where C.activity_date = D.activity_date
            )
            where dio is not null
            order by activity_date
        ) as A,
        (
            select activity_date, dso from
            (
                select
                    C.activity_date,
                    C.avg_receivables / D.revenue * 365 as dso
                from
                (
                    -- Average Receivables
                    select A.activity_date, avg(B.receivables) as avg_receivables from
                    (
                        select activity_date, sum(number) as receivables from
                        (
                            select activity_date, item, number, max(report_date) from BalanceSheet
                            where
                                report_type = 'C'
                                and stock_code = ?
                                and item like '%應收帳款%'
                            group by activity_date, item
                        )
                        group by activity_date
                    ) as A,
                    (
                        select activity_date, sum(number) as receivables from
                        (
                            select activity_date, item, number, max(report_date) from BalanceSheet
                            where
                                report_type = 'C'
                                and stock_code = ?
                                and item like '%應收帳款%'
                            group by activity_date, item
                        )
                        group by activity_date
                    ) as B
                    where B.activity_date <= A.activity_date
                    and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                    group by A.activity_date     
                ) as C,
                (
                    -- Revenue
                    select
                        max(report_date),
                        activity_date,
                        case
                            when strftime('%m', activity_date) = '03' then number * 4/1
                            when strftime('%m', activity_date) = '06' then number * 4/2
                            when strftime('%m', activity_date) = '09' then number * 4/3
                            else number
                        end as revenue
                    from IncomeStmt
                    where
                        report_type = 'C'
                        and stock_code = ?
                        and item = '營業收入合計'
                    group by activity_date
                ) as D
                where C.activity_date = D.activity_date
            )
            where dso is not null
            order by activity_date
        ) as B,
        (
            select activity_date, dpo from
            (
                select
                    C.activity_date,
                    C.avg_payables / D.cogs * 365 as dpo
                from
                (
                    -- Average Payables
                    select A.activity_date, avg(B.payables) as avg_payables from
                    (
                        select activity_date, sum(number) as payables from
                        (
                            select activity_date, item, number, max(report_date) from BalanceSheet
                            where
                                report_type = 'C'
                                and stock_code = ?
                                and item like '%應付帳款%'
                            group by activity_date, item
                        )
                        group by activity_date
                    ) as A,
                    (
                        select activity_date, sum(number) as payables from
                        (
                            select activity_date, item, number, max(report_date) from BalanceSheet
                            where
                                report_type = 'C'
                                and stock_code = ?
                                and item like '%應付帳款%'
                            group by activity_date, item
                        )
                        group by activity_date
                    ) as B
                    where B.activity_date <= A.activity_date
                    and julianday(A.activity_date) <= julianday(B.activity_date, '+3 month')
                    group by A.activity_date     
                ) as C,
                (
                    --COGS
                    select
                        max(report_date),
                        activity_date,
                        case
                            when strftime('%m', activity_date) = '03' then number * 4/1
                            when strftime('%m', activity_date) = '06' then number * 4/2
                            when strftime('%m', activity_date) = '09' then number * 4/3
                            else number
                        end as cogs
                    from IncomeStmt
                    where
                        report_type = 'C'
                        and stock_code = ?
                        and item = '營業成本合計'
                    group by activity_date
                ) as D
                where C.activity_date = D.activity_date
            )
            where dpo is not null
            order by activity_date
        ) as C
        where A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and C.activity_date = A.activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [
            stock_code, stock_code, stock_code,
            stock_code, stock_code, stock_code,
            stock_code, stock_code, stock_code,
        ])