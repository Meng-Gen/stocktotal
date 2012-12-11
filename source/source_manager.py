import datetime
import logging
import sys

import core.base.date_util as date_util
import core.base.logger as logger

class SourceManager():

    def __init__(self):
        self.LOGGER = logging.getLogger()

    def source_stock_code(self):
        import core.source.stock_code_source as source
        s = source.StockCodeSource()
        s.source()
        
    def source_cash_flow_stmt(self, stock, period, content):
        import core.source.cash_flow_stmt_source as source
        s = source.CashFlowStmtSource()        
        begin_date = self.__get_stmt_source_begin_date(period)
        end_date = self.__get_stmt_source_end_date(period)
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            if content == 'all':
                s.source(stock_code, begin_date, end_date)
            elif content == 'no_url':
                s.source_bypass_url(stock_code, begin_date, end_date)
            elif content == 'url':
                s.init_dates(begin_date, end_date)
                s.source_url_to_html(s.HTML_DIR, stock_code)
            
    def source_income_stmt(self, stock, period, content):
        import core.source.income_stmt_source as source
        s = source.IncomeStmtSource()       
        begin_date = self.__get_stmt_source_begin_date(period)
        end_date = self.__get_stmt_source_end_date(period)
        for stock_code in  self.__get_stock_codes(stock):
            if stock_code <= '8938':
                continue
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            
            if content == 'all':
                s.source(stock_code, begin_date, end_date)
            elif content == 'no_url':
                s.source_bypass_url(stock_code, begin_date, end_date)
            elif content == 'url':
                s.init_dates(begin_date, end_date)
                s.source_url_to_html(s.HTML_DIR, stock_code)
        
    def source_balance_sheet(self, stock, period, content):
        import core.source.balance_sheet_source as source
        s = source.BalanceSheetSource()
        begin_date = self.__get_stmt_source_begin_date(period)
        end_date = self.__get_stmt_source_end_date(period)
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            if content == 'all':
                s.source(stock_code, begin_date, end_date)
            elif content == 'no_url':
                s.source_bypass_url(stock_code, begin_date, end_date)
            elif content == 'url':
                s.init_dates(begin_date, end_date)
                s.source_url_to_html(s.HTML_DIR, stock_code)
        
    def source_operating_income(self, period):
        import core.source.operating_income_source as source
        s = source.OperatingIncomeSource()
        begin_date = self.__get_monthly_source_begin_date(period, '2001-06-01')
        end_date = self.__get_monthly_source_end_date(period)
        s.source(begin_date, end_date)

    def source_market_stat(self, period):
        import core.source.market_stat_source as source
        s = source.MarketStatSource()
        begin_date = self.__get_monthly_source_begin_date(period, '1999-01-01')
        end_date = self.__get_monthly_source_end_date(period)
        s.source(begin_date, end_date) 
        
    def source_trading_summary(self, period):
        import core.source.trading_summary_source as source
        s = source.TradingSummarySource()
        begin_date = self.__get_daily_source_begin_date(period, '2004-04-01')
        end_date = self.__get_daily_source_end_date(period)
        s.source(begin_date, end_date)

    def source_listed_co_stat(self, period):
        import core.source.listed_co_stat_source as source
        s = source.ListedCoStatSource()
        begin_date = self.__get_monthly_source_begin_date(period, '1999-03-01')
        end_date = self.__get_monthly_source_end_date(period)
        s.source(begin_date, end_date) 

    def source_capital_structure(self, stock):
        import core.source.capital_structure_source as source
        s = source.CapitalStructureSource()
        begin_date = '1989-01-01'
        end_date = str(date_util.get_this_month())
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            s.source(stock_code, begin_date, end_date) 

    def source_capital_structure_summary(self, stock):
        import core.source.capital_structure_summary_source as source
        s = source.CapitalStructureSummarySource()
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            s.source(stock_code) 

    def source_stock_dividend(self, stock):
        import core.source.stock_dividend_source as source
        s = source.StockDividendSource()
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            s.source(stock_code) 
            
    def source_monthly_trading_info(self, stock, period, content):
        import core.source.monthly_trading_info_source as source
        s = source.MonthlyTradingInfoSource()
        begin_date = self.__get_yearly_source_begin_date(period, '1992-01-01')
        end_date = self.__get_yearly_source_end_date(period)
        for stock_code in  self.__get_stock_codes(stock):
            self.LOGGER.info('''Stock Code: {stock_code}'''.format(stock_code = stock_code))
            if content == 'all':
                s.source(stock_code, begin_date, end_date)
            elif content == 'no_url':
                s.source_bypass_url(stock_code, begin_date, end_date)
            elif content == 'url':
                s.init_dates(begin_date, end_date)
                s.source_url_to_html(s.HTML_DIR, stock_code)
            
    def __get_stock_codes(self, stock):
        if stock == 'all':
            import core.db.query.query_factory as query_factory
            q = query_factory.QueryFactory().stock_code_query()
            return q.query_otc()
            #return q.query_listed_co()
        else:
            return [stock]

    def __get_stmt_source_begin_date(self, period):
        if period == 'all':
            return '2001-03-01'
        elif period == 'recent':
            return str(date_util.get_last_quarter())
        elif period == 'long':
            return str(date_util.get_last_four_quarter())

    def __get_stmt_source_end_date(self, period):
        return str(date_util.get_last_quarter())

    def __get_yearly_source_begin_date(self, period, source_first_year):
        if period == 'all':
            return source_first_year
        elif period == 'recent' or period == 'long':
            return str(date_util.get_last_year_by(date_util.get_this_month()))

    def __get_yearly_source_end_date(self, period):
        return str(date_util.get_this_month())       
        
    def __get_monthly_source_begin_date(self, period, source_first_month):
        if period == 'all':
            return source_first_month
        elif period == 'recent':
            return str(date_util.get_last_month())
        elif period == 'long':
            return str(date_util.get_last_year_by(date_util.get_last_month()))

    def __get_monthly_source_end_date(self, period):
        return str(date_util.get_last_month())
        
    def __get_daily_source_begin_date(self, period, source_first_day):
        if period == 'all':
            return source_first_day
        elif period == 'recent':
            return str(date_util.get_yesterday())
        elif period == 'long':
            return str(date_util.get_last_month())

    def __get_daily_source_end_date(self, period):
        return str(date_util.get_yesterday())        


        
def main():
    logger.config_root(level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', '--target', default='stock_code', help='set target: stock_code, \
            cash_flow_stmt, income_stmt, balance_sheet, \
            market_stat, operating_income, trading_summary, listed_co_stat, \
            capital_structure, capital_structure_summary, stock_dividend, monthly_trading_info')
    parser.add_argument('-s', '--stock', default='all', help='set stock: all, 1101, ...')
    parser.add_argument('-p', '--period', default='recent', help='set period: all, recent, long')
    parser.add_argument('-c', '--content', default='url', help='set source content: all, no_url, url')
    args = parser.parse_args()
    
    m = SourceManager()
    source_map = {
        'stock_code': m.source_stock_code,
        'cash_flow_stmt': m.source_cash_flow_stmt,
        'income_stmt': m.source_income_stmt,
        'balance_sheet': m.source_balance_sheet,
        'operating_income': m.source_operating_income,
        'market_stat': m.source_market_stat,
        'trading_summary': m.source_trading_summary,
        'listed_co_stat': m.source_listed_co_stat,
        'capital_structure': m.source_capital_structure,
        'capital_structure_summary': m.source_capital_structure_summary,
        'stock_dividend': m.source_stock_dividend,
        'monthly_trading_info': m.source_monthly_trading_info,
    }
    assert args.target in source_map
    assert args.period in ['all', 'recent', 'long']
    assert args.content in ['all', 'no_url', 'url']

    if args.target in ['cash_flow_stmt', 'income_stmt', 'balance_sheet', 'monthly_trading_info']:
        source_map[args.target](args.stock, args.period, args.content)
    elif args.target in ['capital_structure', 'capital_structure_summary', 'stock_dividend']:
        source_map[args.target](args.stock)
    elif args.target in ['stock_code']:
        source_map[args.target]()
    else:
        source_map[args.target](args.period)

        
    
if __name__ == '__main__':
    sys.exit(main())
