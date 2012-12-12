--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: capital_structure_summary(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION capital_structure_summary(stock_code text) RETURNS TABLE(activity_date date, spo double precision, spo_ratio double precision, capitalization_earnings double precision, capitalization_earnings_ratio double precision, capitalization_reserve_and_others double precision, capitalization_reserve_and_others_ratio double precision)
    LANGUAGE sql
    AS $_$
select
    T.activity_date,
    T.spo,
    T.spo/T.total as spo_ratio,
    T.capitalization_earnings,
    T.capitalization_earnings/T.total as capitalization_earnings_ratio,
    T.capitalization_reserve_and_others,
    T.capitalization_reserve_and_others/T.total as capitalization_reserve_and_others_ratio
from
(
    select
        activity_date,
        spo,
        capitalization_earnings,
        capitalization_reserve_and_others,
        spo + capitalization_earnings + capitalization_reserve_and_others as total
    from CapitalStructureSummary
    where stock_code = $1
) as T
order by T.activity_date desc
$_$;


ALTER FUNCTION public.capital_structure_summary(stock_code text) OWNER TO stocktotal;

--
-- Name: cash_flow(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION cash_flow(stock_code text) RETURNS TABLE(activity_date date, operating double precision, investing double precision, financing double precision, free_cash_flow double precision, cash_flow double precision, net_profit double precision, net_profit_minus_operating double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as operating,
        B.number as investing,
        C.number as financing,
        D.number as net_profit
    from
        CashFlowStmt as A,
        CashFlowStmt as B,
        CashFlowStmt as C,
        IncomeStmt as D
    where
        A.stock_code = B.stock_code
        and B.stock_code = C.stock_code
        and C.stock_code = D.stock_code
        and A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and C.activity_date = D.activity_date
        and A.report_date = B.report_date
        and B.report_date = C.report_date
        and C.report_date = D.report_date
        and A.item = 'Operating'
        and B.item = 'Investing'
        and C.item = 'Financing'
        and D.item in ('本期淨利(淨損)', '繼續營業單位淨利(淨損)')
        and A.report_type = 'C'
        and B.report_type = 'C'
        and C.report_type = 'C'
        and D.report_type = 'C'
        and A.stock_code = $1
)
select
    T.activity_date,
    T.operating,
    T.investing,
    T.financing,
    T.operating + T.investing as free_cash_flow,
    T.operating + T.investing + T.financing as cash_flow,
    T.net_profit,
    T.net_profit - T.operating as net_profit_minus_operating
from
    T,
    (
        select activity_date, max(report_date) as report_date from T
        group by activity_date
    ) as U
where
    T.activity_date = U.activity_date
    and T.report_date = U.report_date
order by T.activity_date desc
$_$;


ALTER FUNCTION public.cash_flow(stock_code text) OWNER TO stocktotal;

--
-- Name: ccc(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION ccc(stock_code text) RETURNS TABLE(activity_date date, days_inventory_outstanding double precision, days_sales_outstanding double precision, days_payable_outstanding double precision, ccc double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as inventory,
        case
            when date_part('month', A.activity_date) = 3 then B.number * 4/1
            when date_part('month', A.activity_date) = 6 then B.number * 4/2
            when date_part('month', A.activity_date) = 9 then B.number * 4/3
            else B.number
        end as operating_cost,
        case
            when date_part('month', A.activity_date) = 3 then C.number * 4/1
            when date_part('month', A.activity_date) = 6 then C.number * 4/2
            when date_part('month', A.activity_date) = 9 then C.number * 4/3
            else C.number
        end as operating_income,
        D.receivables,
        E.payables
    from
        BalanceSheet as A,
        IncomeStmt as B,
        IncomeStmt as C,
        (
            select D1.activity_date, D1.report_date, sum(D1.number) as receivables from
            (
                select activity_date, report_date, number
                from BalanceSheet
                where report_type = 'C' and stock_code = $1 and item like '%應收帳款%'
            ) as D1
            group by activity_date, report_date
        ) as D,
        (
            select E1.activity_date, E1.report_date, sum(E1.number) as payables from
            (
                select activity_date, report_date, number
                from BalanceSheet
                where report_type = 'C' and stock_code = $1 and item like '%應付帳款%'
            ) as E1
            group by activity_date, report_date
        ) as E
    where
        A.stock_code = B.stock_code
        and B.stock_code = C.stock_code
        and A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and C.activity_date = D.activity_date
        and D.activity_date = E.activity_date
        and A.report_date = B.report_date
        and B.report_date = C.report_date
        and C.report_date = D.report_date
        and D.report_date = E.report_date
        and A.item = '存貨'
        and B.item = '營業成本合計'
        and C.item = '營業收入合計'
        and A.report_type = 'C'
        and B.report_type = 'C'
        and C.report_type = 'C'
        and A.stock_code = $1
        and (A.number != 0 and B.number != 0 and C.number != 0 and D.receivables != 0 and E.payables != 0)
)
select
    Y.activity_date,
    Y.days_inventory_outstanding,
    Y.days_sales_outstanding,
    Y.days_payable_outstanding,
    Y.days_inventory_outstanding + Y.days_sales_outstanding - Y.days_payable_outstanding as ccc
from
(
    select
        T.activity_date,
        V.avg_inventory / T.operating_cost * 365 as days_inventory_outstanding,
        W.avg_receivables / T.operating_income * 365 as days_sales_outstanding,
        X.avg_payables / T.operating_cost * 365 as days_payable_outstanding
    from
        T,
        (
            select activity_date, max(report_date) as report_date from T
            group by activity_date
        ) as U,
        (
            select
                T1.activity_date, T1.report_date, T1.inventory, avg(T2.inventory) as avg_inventory
            from
                T as T1,
                T as T2
            where
                T2.activity_date <= T1.activity_date
                and T1.activity_date <= T2.activity_date + interval '3 month'
            group by T1.activity_date, T1.report_date, T1.inventory
        ) as V,
        (
            select
                T1.activity_date, T1.report_date, T1.receivables, avg(T2.receivables) as avg_receivables
            from
                T as T1,
                T as T2
            where
                T2.activity_date <= T1.activity_date
                and T1.activity_date <= T2.activity_date + interval '3 month'
            group by T1.activity_date, T1.report_date, T1.receivables
        ) as W,
        (
            select
                T1.activity_date, T1.report_date, T1.payables, avg(T2.payables) as avg_payables
            from
                T as T1,
                T as T2
            where
                T2.activity_date <= T1.activity_date
                and T1.activity_date <= T2.activity_date + interval '3 month'
                group by T1.activity_date, T1.report_date, T1.payables
        ) as X
    where
        T.activity_date = U.activity_date
        and U.activity_date = V.activity_date
        and V.activity_date = W.activity_date
        and W.activity_date = X.activity_date
        and T.report_date = U.report_date
        and U.report_date = V.report_date
        and V.report_date = W.report_date
        and W.report_date = X.report_date
        and T.operating_cost != 0
        and T.operating_income != 0
) as Y
order by Y.activity_date desc
$_$;


ALTER FUNCTION public.ccc(stock_code text) OWNER TO stocktotal;

--
-- Name: current_and_rapid_ratio(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION current_and_rapid_ratio(stock_code text) RETURNS TABLE(activity_date date, current_ratio double precision, rapid_ratio double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as current_assets,
        B.number as current_liabilities,
        C.not_rapid as not_rapid
    from
        BalanceSheet as A,
        BalanceSheet as B,
        (
            select
                activity_date,
                report_date,
                sum(number) as not_rapid
            from BalanceSheet
            where
                report_type = 'C'
                and stock_code = $1
                and item in ('存貨', '預付款項', '其他流動資產')
            group by activity_date, report_date
        ) as C
    where
        A.stock_code = B.stock_code
        and A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and A.report_date = B.report_date
        and B.report_date = C.report_date
        and A.item = '流動資產'
        and B.item = '流動負債'
        and A.report_type = 'C'
        and B.report_type = 'C'
        and A.stock_code = $1
        and A.number != 0
        and B.number != 0
)
select
    T.activity_date,
    T.current_assets/T.current_liabilities as current_ratio,
    (T.current_assets - T.not_rapid)/T.current_liabilities as rapid_ratio
from
    T,
    (
        select activity_date, max(report_date) as report_date from T
        group by activity_date
    ) as U
where
    T.activity_date = U.activity_date
    and T.report_date = U.report_date
order by T.activity_date desc
$_$;


ALTER FUNCTION public.current_and_rapid_ratio(stock_code text) OWNER TO stocktotal;

--
-- Name: evaluation_index(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION evaluation_index(stock_code text) RETURNS TABLE(activity_date date, inventory_growth double precision, receivables_growth double precision, gross_profit_growth double precision, sga_growth double precision, payables_growth double precision, operating_income_growth double precision, inventory_index double precision, receivable_index double precision, gross_profit_index double precision, sga_index double precision, payable_index double precision)
    LANGUAGE sql
    AS $_$
with W as
(
    with T as
    (
        select
            A.activity_date,
            A.report_date,
            A.number as inventory,
            B.number as gross_profit,
            C.number as operating_income,
            D.receivables,
            E.payables,
            F.sga
        from
            BalanceSheet as A,
            IncomeStmt as B,
            IncomeStmt as C,
            (
                select D1.activity_date, D1.report_date, sum(D1.number) as receivables from
                (
                    select activity_date, report_date, number
                    from BalanceSheet
                    where report_type = 'C' and stock_code = $1 and item like '%應收帳款%'
                ) as D1
                group by activity_date, report_date
            ) as D,
            (
                select E1.activity_date, E1.report_date, sum(E1.number) as payables from
                (
                    select activity_date, report_date, number
                    from BalanceSheet
                    where report_type = 'C' and stock_code = $1 and item like '%應付帳款%'
                ) as E1
                group by activity_date, report_date
            ) as E,
            (
                select F1.activity_date, F1.report_date, sum(F1.number) as sga from
                (
                    select activity_date, report_date, number
                    from IncomeStmt
                    where report_type = 'C' and stock_code = $1 and item in ('推銷費用', '管理及總務費用')
                ) as F1
                group by activity_date, report_date
            ) as F
        where
            A.stock_code = B.stock_code
            and B.stock_code = C.stock_code
            and A.activity_date = B.activity_date
            and B.activity_date = C.activity_date
            and C.activity_date = D.activity_date
            and D.activity_date = E.activity_date
            and E.activity_date = F.activity_date
            and A.report_date = B.report_date
            and B.report_date = C.report_date
            and C.report_date = D.report_date
            and D.report_date = E.report_date
            and E.report_date = F.report_date
            and A.item = '存貨'
            and B.item = '營業毛利(毛損)'
            and C.item = '營業收入合計'
            and A.report_type = 'C'
            and B.report_type = 'C'
            and C.report_type = 'C'
            and A.stock_code = $1
            and (A.number != 0 and B.number != 0 and C.number != 0 and D.receivables != 0 and E.payables != 0 and F.sga != 0)
    )
    select
        V.activity_date,
        V.inventory_growth,
        V.gross_profit_growth,
        V.operating_income_growth,
        V.receivables_growth,
        V.payables_growth,
        V.sga_growth
    from
        T,
        (
            select activity_date, max(report_date) as report_date from T
            group by activity_date
        ) as U,
        (
            select
                T1.activity_date,
                T1.report_date,
                T1.inventory / avg(T2.inventory) - 1 as inventory_growth,
                T1.gross_profit / avg(T2.gross_profit) - 1 as gross_profit_growth,
                T1.operating_income / avg(T2.operating_income) - 1 as operating_income_growth,
                T1.receivables / avg(T2.receivables) - 1 as receivables_growth,
                T1.payables / avg(T2.payables) - 1 as payables_growth,
                T1.sga / avg(T2.sga) - 1 as sga_growth
            from
                T as T1,
                T as T2
            where
                date_part('month', T1.activity_date) = date_part('month', T2.activity_date)
                and date_part('year', T1.activity_date) - date_part('year', T2.activity_date) in (1, 2)
            group by
                T1.activity_date,
                T1.report_date,
                T1.inventory,
                T1.gross_profit,
                T1.operating_income,
                T1.receivables,
                T1.payables,
                T1.sga
        ) as V
    where
        T.activity_date = U.activity_date
        and U.activity_date = V.activity_date
        and T.report_date = U.report_date
        and U.report_date = V.report_date
)
select
    W.activity_date,
    W.inventory_growth,
    W.receivables_growth,
    W.gross_profit_growth,
    W.sga_growth,
    W.payables_growth,
    W.operating_income_growth,
    W.inventory_growth - W.operating_income_growth as inventory_index,
    W.receivables_growth - W.operating_income_growth as receivable_index,
    W.operating_income_growth - W.gross_profit_growth as gross_profit_index,
    W.sga_growth - W.operating_income_growth as sga_index,
    W.operating_income_growth - W.payables_growth as payable_index
from W
order by W.activity_date desc
$_$;


ALTER FUNCTION public.evaluation_index(stock_code text) OWNER TO stocktotal;

--
-- Name: expected_price_range(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION expected_price_range(stock_code text) RETURNS TABLE(highest_expected_price double precision, lowest_expected_price double precision)
    LANGUAGE sql
    AS $_$
with ExpectedRoeRange as
(
    select * from expected_roe_range($1)
)
select 
    X.roe / Y.avg_highest_expected_roe * X.book_value as highest_expected_price,
    X.roe / Y.avg_lowest_expected_roe * X.book_value as lowest_expected_price
from 
(
    select roe, yearly_highest_price, yearly_lowest_price, book_value from ExpectedRoeRange where activity_year in 
    (
        select max(activity_year) from ExpectedRoeRange
    ) 
) as X,
(
    select 
        avg(highest_expected_roe) as avg_highest_expected_roe, 
        avg(lowest_expected_roe) as avg_lowest_expected_roe
    from ExpectedRoeRange
) as Y
$_$;


ALTER FUNCTION public.expected_price_range(stock_code text) OWNER TO stocktotal;

--
-- Name: expected_roe_range(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION expected_roe_range(stock_code text) RETURNS TABLE(activity_year double precision, roe double precision, yearly_highest_price double precision, yearly_lowest_price double precision, book_value double precision, highest_expected_roe double precision, lowest_expected_roe double precision)
    LANGUAGE sql
    AS $_$
select 
    X.activity_year, 
    X.roe, 
    X.yearly_highest_price, 
    X.yearly_lowest_price, 
    Y.book_value,
    X.roe / X.yearly_highest_price * Y.book_value as highest_expected_roe,
    X.roe / X.yearly_lowest_price * Y.book_value as lowest_expected_roe
from
(
    with YearlyRoe as 
    (
        with Roe as 
        (
            select activity_date, roe from roe($1)
        )
        select activity_date, roe from Roe where activity_date in 
        (
            select A.activity_date from 
            (
                select 
                    date_part('year', activity_date) as activity_year, 
                    max(activity_date) as activity_date
                from Roe group by activity_year
            ) as A
        )
    )
    select 
        A.activity_year,
        A.yearly_highest_price, 
        A.yearly_lowest_price,
        B.roe
    from 
    (
        select 
            date_part('year', activity_date) as activity_year,
            max(high) as yearly_highest_price, 
            min(low) as yearly_lowest_price 
        from HistoricalPrices where stock_code = $1
        group by activity_year
    ) as A,
    YearlyRoe as B
    where A.activity_year = date_part('year', B.activity_date)
) as X,
(
    with BookValue as 
    (
        with T as
        (
            select
                A.activity_date,
                A.report_date,
                A.number as equity,
                B.number as common_stock_capital,
                C.preferred_stock_capital as preferred_stock_capital
            from
                BalanceSheet as A,
                BalanceSheet as B,
                (
                    select
                        activity_date,
                        report_date,
                        sum(number) as preferred_stock_capital
                    from BalanceSheet
                    where
                        report_type = 'C'
                        and stock_code = $1
                        and item in ('少數股權')
                    group by activity_date, report_date
                ) as C
            where
                A.stock_code = B.stock_code
                and A.activity_date = B.activity_date
                and B.activity_date = C.activity_date
                and A.report_date = B.report_date
                and B.report_date = C.report_date
                and A.item = '股東權益總計'
                and B.item = '普通股股本'
                and A.report_type = 'C'
                and B.report_type = 'C'
                and A.stock_code = $1
                and A.number != 0
                and B.number != 0
        )
        select
            T.activity_date,
            (T.equity - T.preferred_stock_capital)/T.common_stock_capital * 10 as book_value
        from
            T,
            (
                select activity_date, max(report_date) as report_date from T
                group by activity_date
            ) as U
        where
            T.activity_date = U.activity_date
            and T.report_date = U.report_date
    )
    select date_part('year', activity_date) as activity_year, book_value from BookValue where activity_date in 
    (
        select A.activity_date from 
        (
            select 
                date_part('year', activity_date) as activity_year, 
                max(activity_date) as activity_date
            from BookValue group by activity_year
        ) as A
    )
) as Y
where X.activity_year = Y.activity_year
order by X.activity_year desc
$_$;


ALTER FUNCTION public.expected_roe_range(stock_code text) OWNER TO stocktotal;

--
-- Name: financial_structure(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION financial_structure(stock_code text) RETURNS TABLE(activity_date date, equity_ratio double precision, liabilities_ratio double precision, equity_multiplier double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as assets,
        B.number as liabilities,
        C.number as equity
    from
        BalanceSheet as A,
        BalanceSheet as B,
        BalanceSheet as C
    where
    A.stock_code = B.stock_code
    and B.stock_code = C.stock_code
    and A.activity_date = B.activity_date
    and B.activity_date = C.activity_date
    and A.report_date = B.report_date
    and B.report_date = C.report_date
    and A.item = '資產總計'
    and B.item = '負債總計'
    and C.item = '股東權益總計'
    and A.report_type = 'C'
    and B.report_type = 'C'
    and C.report_type = 'C'
    and A.number != 0
    and B.number != 0
    and C.number != 0
    and A.stock_code = $1
)
select
    V.activity_date,
    V.equity/V.assets as equity_ratio,
    V.liabilities/V.assets as liabilities_ratio,
    V.assets/V.equity as equity_multiplier
from
(
    select
        T.activity_date,
        T.assets,
        T.equity,
        T.liabilities
    from
        T,
        (
            select activity_date, max(report_date) as report_date from T
            group by activity_date
        ) as U
    where
        T.activity_date = U.activity_date
        and T.report_date = U.report_date
) as V
order by V.activity_date desc
$_$;


ALTER FUNCTION public.financial_structure(stock_code text) OWNER TO stocktotal;

--
-- Name: long_term_investments(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION long_term_investments(stock_code text) RETURNS TABLE(activity_date date, long_term_investments double precision, assets double precision, long_term_investments_ratio double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as long_term_investments,
        B.number as assets
    from
        BalanceSheet as A,
        BalanceSheet as B
    where
        A.stock_code = B.stock_code
        and A.activity_date = B.activity_date
        and A.report_date = B.report_date
        and A.item in ('長期投資合計', '基金及投資')
        and B.item = '資產總計'
        and A.report_type = 'C'
        and B.report_type = 'C'
        and A.stock_code = $1
)
select
    T.activity_date,
    T.long_term_investments,
    T.assets,
    T.long_term_investments/T.assets as long_term_investments_ratio
from
    T,
    (
        select activity_date, max(report_date) as report_date from T
        group by activity_date
    ) as U
where
    T.activity_date = U.activity_date
    and T.report_date = U.report_date
    and T.assets != 0
order by T.activity_date
$_$;


ALTER FUNCTION public.long_term_investments(stock_code text) OWNER TO stocktotal;

--
-- Name: nonoperating_income(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION nonoperating_income(stock_code text) RETURNS TABLE(activity_date date, non_operating_income_ratio double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as operating_income,
        B.number as non_operating_income
    from
        IncomeStmt as A,
        IncomeStmt as B
    where
        A.stock_code = B.stock_code
        and A.activity_date = B.activity_date
        and A.report_date = B.report_date
        and A.item in ('繼續營業部門稅前淨利(淨損)', '繼續營業單位稅前淨利(淨損)')
        and B.item in ('營業外收入合計', '營業外收入及利益')
        and A.report_type = 'C'
        and B.report_type = 'C'
        and A.stock_code = $1
)
select
    T.activity_date,
    T.non_operating_income/T.operating_income as non_operating_income_ratio
from
    T,
    (
        select activity_date, max(report_date) as report_date from T
        group by activity_date
    ) as U
where
    T.activity_date = U.activity_date
    and T.report_date = U.report_date
    and T.operating_income != 0
order by T.activity_date
$_$;


ALTER FUNCTION public.nonoperating_income(stock_code text) OWNER TO stocktotal;

--
-- Name: operating_income(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION operating_income(stock_code text) RETURNS TABLE(activity_date date, income double precision, income_yoy double precision, accumlated_income double precision, accumlated_income_yoy double precision, ma3_income double precision, ma12_income double precision)
    LANGUAGE sql
    AS $_$
with W as
(
    with T as
    (
        select A.activity_date, A.income
        from
            (
                select activity_date, report_date, income
                from OperatingIncome
                where stock_code = $1
            ) as A,
            (
                select activity_date, max(report_date) as latest_report_date
                from OperatingIncome
                where stock_code = $1
                group by activity_date
            ) as B
        where A.activity_date = B.activity_date and A.report_date = B.latest_report_date
        order by A.activity_date
    )
    select
        V.activity_date,
        V.income,
        V.accumlated_income,
        V.ma3_income,
        V.ma12_income
    from
    (
        select T.activity_date, T.income, U.accumlated_income, MA3.ma3_income, MA12.ma12_income
        from
            T,
            (
                select T1.activity_date, sum(T2.income) as accumlated_income
                from T as T1, T as T2
                where
                    T2.activity_date <= T1.activity_date
                    and date_part('year', T1.activity_date) = date_part('year', T2.activity_date)
                group by T1.activity_date
            ) as U,
            (
                select T1.activity_date, avg(T2.income) as ma3_income
                from T as T1, T as T2
                where
                    T2.activity_date <= T1.activity_date
                    and T1.activity_date < T2.activity_date + interval '3 month'
                group by T1.activity_date
            ) as MA3,
            (
                select T1.activity_date, avg(T2.income) as ma12_income
                from T as T1, T as T2
                where
                    T2.activity_date <= T1.activity_date
                    and T1.activity_date < T2.activity_date + interval '12 month'
                group by T1.activity_date
            ) as MA12
        where
            T.activity_date = U.activity_date
            and T.activity_date = MA3.activity_date
            and T.activity_date = MA12.activity_date
    ) as V
)
select
    W.activity_date,
    W.income,
    X.income_yoy,
    W.accumlated_income,
    X.accumlated_income_yoy,
    W.ma3_income,
    W.ma12_income
from
    W,
    (
        select
            W1.activity_date,
            W2.income / W1.income - 1 as income_yoy,
            W2.accumlated_income / W1.accumlated_income - 1 as accumlated_income_yoy
        from
            W as W1,
            W as W2
        where
            date_part('year', W2.activity_date) = date_part('year', W1.activity_date) + 1
            and date_part('month', W1.activity_date) = date_part('month', W2.activity_date)
            and W1.income != 0
            and W1.accumlated_income != 0
    ) as X
where
    W.activity_date = X.activity_date
$_$;


ALTER FUNCTION public.operating_income(stock_code text) OWNER TO stocktotal;

--
-- Name: profit_margin(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION profit_margin(stock_code text) RETURNS TABLE(activity_date date, gross_profit_margin double precision, operating_profit_margin double precision, net_profit_margin double precision)
    LANGUAGE sql
    AS $_$
with T as
(
    select
        A.activity_date,
        A.report_date,
        A.number as gross_profit,
        B.number as operating_profit,
        C.number as net_profit,
        D.number as operating_income
    from
        IncomeStmt as A,
        IncomeStmt as B,
        IncomeStmt as C,
        IncomeStmt as D
    where
        A.stock_code = B.stock_code
        and B.stock_code = C.stock_code
        and C.stock_code = D.stock_code
        and A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and C.activity_date = D.activity_date
        and A.report_date = B.report_date
        and B.report_date = C.report_date
        and C.report_date = D.report_date
        and A.item = '營業毛利(毛損)'
        and B.item = '營業淨利(淨損)'
        and C.item = '合併總損益'
        and D.item = '營業收入合計'
        and A.report_type = 'C'
        and B.report_type = 'C'
        and C.report_type = 'C'
        and D.report_type = 'C'
        and A.stock_code = $1
)
select
    T.activity_date,
    T.gross_profit / T.operating_income as gross_profit_margin,
    T.operating_profit / T.operating_income as operating_profit_margin,
    T.net_profit / T.operating_income as net_profit_margin
from
    T,
    (
        select activity_date, max(report_date) as report_date from T
        group by activity_date
    ) as U
where
    T.activity_date = U.activity_date
    and T.report_date = U.report_date
    and T.operating_income != 0
order by T.activity_date
$_$;


ALTER FUNCTION public.profit_margin(stock_code text) OWNER TO stocktotal;

--
-- Name: roe(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION roe(stock_code text) RETURNS TABLE(activity_date date, roe double precision, net_profit_margin double precision, total_assets_turnover double precision, equity_multiplier double precision)
    LANGUAGE sql
    AS $_$
with T as
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
        A.stock_code = B.stock_code
        and B.stock_code = C.stock_code
        and C.stock_code = D.stock_code
        and A.activity_date = B.activity_date
        and B.activity_date = C.activity_date
        and C.activity_date = D.activity_date
        and A.report_date = B.report_date
        and B.report_date = C.report_date
        and C.report_date = D.report_date
        and A.item = '股東權益總計'
        and B.item = '合併總損益'
        and C.item = '營業收入合計'
        and D.item = '資產總計'
        and A.report_type = 'C'
        and B.report_type = 'C'
        and C.report_type = 'C'
        and D.report_type = 'C'
        and A.stock_code = $1
        and A.number != 0
        and B.number != 0
        and C.number != 0
        and D.number != 0
)
select
    V.activity_date,
    V.annual_adjusted_net_income/V.shareholder_equity as roe,
    V.annual_adjusted_net_income/V.annual_adjusted_operating_income as net_profit_margin,
    V.annual_adjusted_operating_income/V.total_assets as total_assets_turnover,
    V.total_assets/V.shareholder_equity as equity_multiplier
from
(
    select
        T.activity_date,
        T.shareholder_equity,
        case
            when date_part('month', T.activity_date) = 3 then T.net_income * 4/1
            when date_part('month', T.activity_date) = 6 then T.net_income * 4/2
            when date_part('month', T.activity_date) = 9 then T.net_income * 4/3
            else T.net_income
        end as annual_adjusted_net_income,
        case
            when date_part('month', T.activity_date) = 3 then T.operating_income * 4/1
            when date_part('month', T.activity_date) = 6 then T.operating_income * 4/2
            when date_part('month', T.activity_date) = 9 then T.operating_income * 4/3
            else T.operating_income
        end as annual_adjusted_operating_income,
        T.total_assets
    from
        T,
        (
            select activity_date, max(report_date) as report_date from T
            group by activity_date
        ) as U
    where
        T.activity_date = U.activity_date
        and T.report_date = U.report_date
    order by T.activity_date
) as V
order by V.activity_date desc
$_$;


ALTER FUNCTION public.roe(stock_code text) OWNER TO stocktotal;

--
-- Name: stock_dividend(text); Type: FUNCTION; Schema: public; Owner: stocktotal
--

CREATE FUNCTION stock_dividend(stock_code text) RETURNS TABLE(activity_date date, cash_dividend double precision, stock_dividend_from_retained_earnings double precision, stock_dividend_from_capital_reserve double precision, stock_dividend double precision, total_dividend double precision, profit_sharing_percentage double precision)
    LANGUAGE sql
    AS $_$
select
    activity_date,
    cash_dividend,
    stock_dividend_from_retained_earnings,
    stock_dividend_from_capital_reserve,
    stock_dividend,
    total_dividend,
    profit_sharing_percentage
from StockDividend
where stock_code = $1
order by activity_date desc
$_$;


ALTER FUNCTION public.stock_dividend(stock_code text) OWNER TO stocktotal;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: balancesheet; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE balancesheet (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    report_type character(1) NOT NULL,
    report_date date NOT NULL,
    activity_date date NOT NULL,
    item text NOT NULL,
    number double precision NOT NULL
);


ALTER TABLE public.balancesheet OWNER TO stocktotal;

--
-- Name: capitalstructure; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE capitalstructure (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    debut character(1),
    par_value double precision,
    authorized_capital_stock double precision,
    authorized_capital double precision,
    paidin_capital_stock double precision,
    paidin_capital double precision,
    ipo double precision,
    spo double precision,
    capitalization_capital_reserve double precision,
    capitalization_retained_earnings double precision,
    by_acquisition double precision,
    capital_reduction double precision,
    capital_others text,
    capital_other_than_cash text,
    note text
);


ALTER TABLE public.capitalstructure OWNER TO stocktotal;

--
-- Name: capitalstructuresummary; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE capitalstructuresummary (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    spo double precision,
    capitalization_earnings double precision,
    capitalization_reserve_and_others double precision
);


ALTER TABLE public.capitalstructuresummary OWNER TO stocktotal;

--
-- Name: cashflowstmt; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE cashflowstmt (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    report_type character(1) NOT NULL,
    report_date date NOT NULL,
    activity_date date NOT NULL,
    item text NOT NULL,
    number double precision NOT NULL
);


ALTER TABLE public.cashflowstmt OWNER TO stocktotal;

--
-- Name: historicalprices; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE historicalprices (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    open double precision,
    high double precision,
    low double precision,
    close double precision,
    volume double precision,
    adj_close double precision
);


ALTER TABLE public.historicalprices OWNER TO stocktotal;

--
-- Name: incomestmt; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE incomestmt (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    report_type character(1) NOT NULL,
    report_date date NOT NULL,
    activity_date date NOT NULL,
    item text NOT NULL,
    number double precision NOT NULL
);


ALTER TABLE public.incomestmt OWNER TO stocktotal;

--
-- Name: listedcostatistics; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE listedcostatistics (
    creation_dt timestamp without time zone DEFAULT now(),
    report_date date NOT NULL,
    stock_code text NOT NULL,
    latest_price double precision,
    per double precision,
    yield double precision,
    pbr double precision
);


ALTER TABLE public.listedcostatistics OWNER TO stocktotal;

--
-- Name: listedcotradinginfo; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE listedcotradinginfo (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    highest_price double precision,
    lowest_price double precision,
    weighted_average_price double precision,
    trans double precision,
    trade_value double precision,
    trade_volume double precision,
    turnover_ratio double precision
);


ALTER TABLE public.listedcotradinginfo OWNER TO stocktotal;

--
-- Name: marketstatistics; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE marketstatistics (
    creation_dt timestamp without time zone DEFAULT now(),
    report_date date NOT NULL,
    activity_date date NOT NULL,
    report_type text NOT NULL,
    total_trading_value double precision,
    listed_co_number double precision,
    capital_issued double precision,
    total_listed_shares double precision,
    market_capitalization double precision,
    trading_volume double precision,
    trading_value double precision,
    trans_number double precision,
    average_taiex double precision,
    volume_turnover_rate double precision,
    per double precision,
    dividend_yield double precision,
    pbr double precision,
    trading_days integer
);


ALTER TABLE public.marketstatistics OWNER TO stocktotal;

--
-- Name: operatingincome; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE operatingincome (
    creation_dt timestamp without time zone DEFAULT now(),
    report_date date NOT NULL,
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    income double precision
);


ALTER TABLE public.operatingincome OWNER TO stocktotal;

--
-- Name: stockcode; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE stockcode (
    creation_dt timestamp without time zone DEFAULT now(),
    code text,
    name text,
    isin_code text,
    listing_date date,
    market_category text,
    industry_category text,
    cfi_code text
);


ALTER TABLE public.stockcode OWNER TO stocktotal;

--
-- Name: stockdividend; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE stockdividend (
    creation_dt timestamp without time zone DEFAULT now(),
    stock_code text NOT NULL,
    activity_date date NOT NULL,
    cash_dividend double precision,
    stock_dividend_from_retained_earnings double precision,
    stock_dividend_from_capital_reserve double precision,
    stock_dividend double precision,
    total_dividend double precision,
    profit_sharing_percentage double precision
);


ALTER TABLE public.stockdividend OWNER TO stocktotal;

--
-- Name: tradingsummary; Type: TABLE; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE TABLE tradingsummary (
    creation_dt timestamp without time zone DEFAULT now(),
    trading_date date NOT NULL,
    item text NOT NULL,
    buy double precision NOT NULL,
    sell double precision NOT NULL,
    diff double precision NOT NULL
);


ALTER TABLE public.tradingsummary OWNER TO stocktotal;

--
-- Name: balancesheet_stock_code_report_type_report_date_activity_da_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY balancesheet
    ADD CONSTRAINT balancesheet_stock_code_report_type_report_date_activity_da_key UNIQUE (stock_code, report_type, report_date, activity_date, item);


--
-- Name: capitalstructure_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY capitalstructure
    ADD CONSTRAINT capitalstructure_stock_code_activity_date_key UNIQUE (stock_code, activity_date);


--
-- Name: capitalstructuresummary_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY capitalstructuresummary
    ADD CONSTRAINT capitalstructuresummary_stock_code_activity_date_key UNIQUE (stock_code, activity_date);


--
-- Name: cashflowstmt_stock_code_report_type_report_date_activity_da_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY cashflowstmt
    ADD CONSTRAINT cashflowstmt_stock_code_report_type_report_date_activity_da_key UNIQUE (stock_code, report_type, report_date, activity_date, item);


--
-- Name: historicalprices_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY historicalprices
    ADD CONSTRAINT historicalprices_stock_code_activity_date_key UNIQUE (stock_code, activity_date);


--
-- Name: incomestmt_stock_code_report_type_report_date_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY incomestmt
    ADD CONSTRAINT incomestmt_stock_code_report_type_report_date_activity_date_key UNIQUE (stock_code, report_type, report_date, activity_date, item);


--
-- Name: listedcostatistics_report_date_stock_code_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY listedcostatistics
    ADD CONSTRAINT listedcostatistics_report_date_stock_code_key UNIQUE (report_date, stock_code);


--
-- Name: listedcotradinginfo_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY listedcotradinginfo
    ADD CONSTRAINT listedcotradinginfo_stock_code_activity_date_key UNIQUE (stock_code, activity_date);


--
-- Name: marketstatistics_report_date_activity_date_report_type_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY marketstatistics
    ADD CONSTRAINT marketstatistics_report_date_activity_date_report_type_key UNIQUE (report_date, activity_date, report_type);


--
-- Name: operatingincome_report_date_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY operatingincome
    ADD CONSTRAINT operatingincome_report_date_stock_code_activity_date_key UNIQUE (report_date, stock_code, activity_date);


--
-- Name: stockcode_code_name_isin_code_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY stockcode
    ADD CONSTRAINT stockcode_code_name_isin_code_key UNIQUE (code, name, isin_code);


--
-- Name: stockdividend_stock_code_activity_date_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY stockdividend
    ADD CONSTRAINT stockdividend_stock_code_activity_date_key UNIQUE (stock_code, activity_date);


--
-- Name: tradingsummary_trading_date_item_key; Type: CONSTRAINT; Schema: public; Owner: stocktotal; Tablespace: 
--

ALTER TABLE ONLY tradingsummary
    ADD CONSTRAINT tradingsummary_trading_date_item_key UNIQUE (trading_date, item);


--
-- Name: ix_balance_sheet_item; Type: INDEX; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE INDEX ix_balance_sheet_item ON balancesheet USING btree (item);


--
-- Name: ix_cash_flow_stmt_item; Type: INDEX; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE INDEX ix_cash_flow_stmt_item ON cashflowstmt USING btree (item);


--
-- Name: ix_income_stmt_item; Type: INDEX; Schema: public; Owner: stocktotal; Tablespace: 
--

CREATE INDEX ix_income_stmt_item ON incomestmt USING btree (item);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: balancesheet; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE balancesheet FROM PUBLIC;
REVOKE ALL ON TABLE balancesheet FROM stocktotal;
GRANT ALL ON TABLE balancesheet TO stocktotal;
GRANT ALL ON TABLE balancesheet TO PUBLIC;


--
-- Name: capitalstructure; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE capitalstructure FROM PUBLIC;
REVOKE ALL ON TABLE capitalstructure FROM stocktotal;
GRANT ALL ON TABLE capitalstructure TO stocktotal;
GRANT ALL ON TABLE capitalstructure TO PUBLIC;


--
-- Name: capitalstructuresummary; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE capitalstructuresummary FROM PUBLIC;
REVOKE ALL ON TABLE capitalstructuresummary FROM stocktotal;
GRANT ALL ON TABLE capitalstructuresummary TO PUBLIC;


--
-- Name: cashflowstmt; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE cashflowstmt FROM PUBLIC;
REVOKE ALL ON TABLE cashflowstmt FROM stocktotal;
GRANT ALL ON TABLE cashflowstmt TO stocktotal;
GRANT ALL ON TABLE cashflowstmt TO PUBLIC;


--
-- Name: historicalprices; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE historicalprices FROM PUBLIC;
REVOKE ALL ON TABLE historicalprices FROM stocktotal;
GRANT ALL ON TABLE historicalprices TO stocktotal;
GRANT ALL ON TABLE historicalprices TO PUBLIC;


--
-- Name: incomestmt; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE incomestmt FROM PUBLIC;
REVOKE ALL ON TABLE incomestmt FROM stocktotal;
GRANT ALL ON TABLE incomestmt TO stocktotal;
GRANT ALL ON TABLE incomestmt TO PUBLIC;


--
-- Name: listedcostatistics; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE listedcostatistics FROM PUBLIC;
REVOKE ALL ON TABLE listedcostatistics FROM stocktotal;
GRANT ALL ON TABLE listedcostatistics TO PUBLIC;


--
-- Name: listedcotradinginfo; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE listedcotradinginfo FROM PUBLIC;
REVOKE ALL ON TABLE listedcotradinginfo FROM stocktotal;
GRANT ALL ON TABLE listedcotradinginfo TO stocktotal;
GRANT ALL ON TABLE listedcotradinginfo TO PUBLIC;


--
-- Name: marketstatistics; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE marketstatistics FROM PUBLIC;
REVOKE ALL ON TABLE marketstatistics FROM stocktotal;
GRANT ALL ON TABLE marketstatistics TO PUBLIC;


--
-- Name: operatingincome; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE operatingincome FROM PUBLIC;
REVOKE ALL ON TABLE operatingincome FROM stocktotal;
GRANT ALL ON TABLE operatingincome TO PUBLIC;


--
-- Name: stockcode; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE stockcode FROM PUBLIC;
REVOKE ALL ON TABLE stockcode FROM stocktotal;
GRANT ALL ON TABLE stockcode TO stocktotal;
GRANT ALL ON TABLE stockcode TO PUBLIC;


--
-- Name: stockdividend; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE stockdividend FROM PUBLIC;
REVOKE ALL ON TABLE stockdividend FROM stocktotal;
GRANT ALL ON TABLE stockdividend TO PUBLIC;


--
-- Name: tradingsummary; Type: ACL; Schema: public; Owner: stocktotal
--

REVOKE ALL ON TABLE tradingsummary FROM PUBLIC;
REVOKE ALL ON TABLE tradingsummary FROM stocktotal;
GRANT ALL ON TABLE tradingsummary TO PUBLIC;


--
-- PostgreSQL database dump complete
--

