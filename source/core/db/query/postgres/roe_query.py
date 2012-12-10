# coding: big5

from . import query

class RoeQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    """
    (annual adjusted) ROE 
    = net income / shareholder equity
    = ( net income / operating income ) 
      x ( operating income / total assets )
      x ( total assets / shareholder equity )
    = ( net profit margin ) x ( total assets turnover ) x ( equity multiplier )

    Refernece: 郭恭克, 獵豹財務長投資魔法書 (ISBN：9789868340091)
    """
    
    def query_roe(self, stock_code):
        SQL_SELECT = \
        '''
        select 
        B.activity_date, 
        case
            when date_part('month', B.activity_date) = 3 then B.roe * 4/1
            when date_part('month', B.activity_date) = 6 then B.roe * 4/2
            when date_part('month', B.activity_date) = 9 then B.roe * 4/3
            else B.roe
        end as annual_adjusted_roe
        from
        (
            select A.activity_date, A.roe, max(A.report_date) from
            (
                select E.activity_date, I.number / E.number as roe, E.report_date
                    from BalanceSheet as E
                inner join
                    IncomeStmt as I
                on E.stock_code = I.stock_code
                and E.activity_date = I.activity_date
                and E.item = '股東權益總計'
                and I.item = '合併總損益'
                and E.report_type = 'C'
                and I.report_type = 'C'
                and E.stock_code = ?
                and E.number <> 0
            ) as A
            group by A.activity_date, A.roe
            order by A.activity_date
        ) as B
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    """
    net profit margin = net income / operating income
    """
    def query_net_profit_margin(self, stock_code):
        SQL_SELECT = \
        '''
        select B.activity_date, B.net_profit_margin from
        (
            select A.activity_date, A.net_profit_margin, max(A.report_date) from
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
                and I.item = '合併總損益'
                and O.item = '營業收入合計'
                and I.report_type = 'C'
                and O.report_type = 'C'
                and I.stock_code = ?
                and O.number <> 0
            ) as A
            group by A.activity_date, A.net_profit_margin
            order by A.activity_date
        ) as B
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    """
    (annual adjusted) total assets turnover = operating income / total assets
    """
    def query_total_assets_turnover(self, stock_code):
        SQL_SELECT = \
        '''
        select B.activity_date, 
        case
            when date_part('month', B.activity_date) = 3 then B.total_assets_turnover * 4/1
            when date_part('month', B.activity_date) = 6 then B.total_assets_turnover * 4/2
            when date_part('month', B.activity_date) = 9 then B.total_assets_turnover * 4/3
            else B.total_assets_turnover
        end as annual_adjusted_total_assets_turnover
        from
        (
            select C.activity_date, C.total_assets_turnover, max(C.report_date) from
            (
                select
                A.activity_date,
                O.number / A.number as total_assets_turnover,
                A.report_date
                from BalanceSheet as A
                inner join
                IncomeStmt as O
                on A.stock_code = O.stock_code
                and A.activity_date = O.activity_date
                and A.item = '資產總計'
                and O.item = '營業收入合計'
                and A.report_type = 'C'
                and O.report_type = 'C'
                and A.stock_code = ?
                and A.number <> 0
            ) as C
            group by C.activity_date, C.total_assets_turnover
            order by C.activity_date
        ) as B
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    """
    equity multiplier = total assets / shareholder equity
    """
    def query_equity_multiplier(self, stock_code):
        SQL_SELECT = \
        '''
        select B.activity_date, B.equity_multiplier from
        (
            select A.activity_date, A.equity_multiplier, max(A.report_date) from
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
                and E.number <> 0
            ) as A
            group by A.activity_date, A.equity_multiplier
            order by A.activity_date
        ) as B
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
"""
select 
    T.activity_date, 
    T.shareholder_equity, 
    case
        when date_part('month', T.activity_date) = 3 then T.net_income * 4/1
        when date_part('month', T.activity_date) = 6 then T.net_income * 4/2
        when date_part('month', T.activity_date) = 9 then T.net_income * 4/3
        else T.net_income
    end as annual_adjusted_net_income,
    T.operating_income,
    T.total_assets,
    max(T.report_date)
from
(
    select 
        A.activity_date, 
        A.report_date,
        A.number as shareholder_equity, 
        B.number as net_income, 
        C.number as operating_income,
        D.number as total_assets
    from  
        BalanceSheet as A,
        IncomeStmt as B,
        IncomeStmt as C,
        BalanceSheet as D
    where
    A.stock_code = B.stock_code and B.stock_code = C.stock_code and C.stock_code = D.stock_code
    and A.activity_date = B.activity_date and B.activity_date = C.activity_date and C.activity_date = D.activity_date
    and A.item = '股東權益總計' 
    and B.item = '合併總損益' 
    and C.item = '營業收入合計'
    and D.item = '資產總計'
    and A.report_type = 'C'
    and B.report_type = 'C'
    and C.report_type = 'C'
    and D.report_type = 'C'
    and A.stock_code = '2498'
) AS T
where 
    T.shareholder_equity != 0
    and T.net_income != 0
    and T.operating_income != 0
    and T.total_assets != 0
group by 
    T.activity_date, 
    T.shareholder_equity, 
    T.net_income, 
    T.operating_income,
    T.total_assets
order by T.activity_date

"""