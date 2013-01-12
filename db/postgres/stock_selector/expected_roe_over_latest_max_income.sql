-- Drop old one
DROP TABLE IF EXISTS ExpectedRoeOverLatestMaxIncome;

-- Create new one
CREATE TEMPORARY TABLE ExpectedRoeOverLatestMaxIncome
(
    stock_code text NOT NULL,
    expected_roe double precision
);

-- Populate
DO $$DECLARE r record;
BEGIN
    FOR r IN select stock_code from latest_stock_code_with_max_income()
    LOOP
        insert into ExpectedRoeOverLatestMaxIncome(stock_code, expected_roe)
        select
            r.stock_code, T.expected_roe
        from 
        (
            select latest_expected_roe as expected_roe from latest_expected_roe(r.stock_code)
        ) as T;
    END LOOP;
END$$;

-- Query
select stock_code, expected_roe from ExpectedRoeOverLatestMaxIncome