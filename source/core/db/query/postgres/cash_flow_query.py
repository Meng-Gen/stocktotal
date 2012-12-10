from . import query

class CashFlowQuery(query.Query):

    def __init__(self):
        query.Query.__init__(self)

    def query_operating_activity(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, number from
        (
            select activity_date, number, max(report_date) from CashFlowStmt where 
            report_type = 'C' 
            and stock_code = ?
            and item = 'Operating'
            group by activity_date, item
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_investing_activity(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, number from
        (
            select activity_date, number, max(report_date) from CashFlowStmt where 
            report_type = 'C' 
            and stock_code = ?
            and item = 'Investing'
            group by activity_date, item
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])

    def query_free_cash_flow(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, sum(number) as free_cash_flow from
        (
            select *, max(report_date) from CashFlowStmt where 
            report_type = 'C' 
            and stock_code = ?
            and item in ('Operating', 'Investing')
            group by activity_date, item
        )
        group by activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])
        
    def query_financing_activity(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, number from
        (
            select activity_date, number, max(report_date) from CashFlowStmt where 
            report_type = 'C' 
            and stock_code = ?
            and item = 'Financing'
            group by activity_date, item
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code]) 

    def query_cash_flow(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, sum(number) as total from
        (
            select activity_date, number, item, max(report_date) from CashFlowStmt where 
            report_type = 'C' 
            and stock_code = ?
            group by activity_date, item
        )
        group by activity_date
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code])             
        
    def query_net_profit_minus_cash_flow(self, stock_code):
        SQL_SELECT = \
        '''
        select activity_date, net_profit_minus_cash_flow from
        (
            select activity_date, net_profit_minus_cash_flow, max(report_date) from
            (
                select
                A.activity_date,
                A.number - B.total as net_profit_minus_cash_flow,
                A.report_date
                from IncomeStmt as A,
                (
                    select activity_date, sum(number) as total from
                    (
                        select activity_date, number, item, max(report_date) from CashFlowStmt where 
                        report_type = 'C' 
                        and stock_code = ?
                        group by activity_date, item
                    )
                    group by activity_date
                ) as B
                where A.stock_code = ?
                and A.activity_date = B.activity_date
                and A.item in ('本期淨利(淨損)', '繼續營業單位淨利(淨損)')
                and A.report_type = 'C'
            )
            group by activity_date
            order by activity_date
        )
        '''
        return self.exec_query_series(SQL_SELECT, [stock_code, stock_code])           