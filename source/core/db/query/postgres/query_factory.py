# coding: utf-8

class QueryFactory():
    @staticmethod
    def roe_query():
        from . import roe_query
        return roe_query.RoeQuery()

    @staticmethod
    def financial_structure_query():
        from . import financial_structure_query
        return financial_structure_query.FinancialStructureQuery()

    @staticmethod
    def current_and_quick_ratio_query():
        from . import current_and_quick_ratio_query
        return current_and_quick_ratio_query.CurrentAndQuickRatioQuery()

    @staticmethod
    def non_operating_income_query():
        from . import non_operating_income_query
        return non_operating_income_query.NonOperatingIncomeQuery()

    @staticmethod
    def long_term_investments_query():
        from . import long_term_investments_query
        return long_term_investments_query.LongTermInvestmentsQuery()

    @staticmethod
    def operating_income_query():
        from . import operating_income_query
        return operating_income_query.OperatingIncomeQuery()

    @staticmethod
    def profit_margin_query():
        from . import profit_margin_query
        return profit_margin_query.ProfitMarginQuery()

    @staticmethod
    def cash_flow_query():
        from . import cash_flow_query
        return cash_flow_query.CashFlowQuery()

    @staticmethod
    def ccc_query():
        from . import ccc_query
        return ccc_query.CccQuery()

    @staticmethod
    def evaluation_indicator_query():
        from . import evaluation_indicator_query
        return evaluation_indicator_query.EvaluationIndicatorQuery()

    @staticmethod
    def stock_code_query():
        from . import stock_code_query
        return stock_code_query.StockCodeQuery()
        