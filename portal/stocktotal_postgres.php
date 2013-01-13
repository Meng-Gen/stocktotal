<?php    class StocktotalPostgres {            public function __construct() {            $this->conn = pg_connect($this->conn_str) or die("Could not connect to server: " . pg_last_error());        }        public function __destruct() {            pg_close($this->conn);         }        public function query_roe($stock_code) {            $sql_cmd = "select * from roe('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'roe' => round($row[1], 2),                     'net_profit_margin' => round($row[2], 2),                     'total_assets_turnover' => round($row[3], 2),                     'equity_multiplier' => round($row[4], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_financial_structure($stock_code) {            $sql_cmd = "select * from financial_structure('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'equity_ratio' => round($row[1], 2),                     'liabilities_ratio' => round($row[2], 2),                     'equity_multiplier' => round($row[3], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_current_and_rapid_ratio($stock_code) {            $sql_cmd = "select * from current_and_rapid_ratio('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'current_ratio' => round($row[1], 2),                     'rapid_ratio' => round($row[2], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_nonoperating_income($stock_code) {            $sql_cmd = "select * from nonoperating_income('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'non_operating_income_ratio' => round($row[1], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_long_term_investments($stock_code) {            $sql_cmd = "select * from long_term_investments('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'long_term_investments' => $row[1],                    'assets' => $row[2],                    'long_term_investments_ratio' => round($row[3], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_operating_income($stock_code) {            $sql_cmd = "select * from operating_income('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'income' => $row[1],                     'income_yoy' => round($row[2], 2),                    'accumlated_income' => $row[3],                    'accumlated_income_yoy' => round($row[4], 2),                     'ma3_income' => round($row[5]),                    'ma12_income' => round($row[6])                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_accumlated_income_yoy($stock_code) {            $sql_cmd = "select * from accumlated_income_yoy('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'accumlated_income_yoy' => round($row[1], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_profit_margin($stock_code) {            $sql_cmd = "select * from profit_margin('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'gross_profit_margin' => round($row[1], 2),                     'operating_profit_margin' => round($row[2], 2),                     'net_profit_margin' => round($row[3], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_cash_flow($stock_code) {            $sql_cmd = "select * from cash_flow('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'operating' => $row[1],                     'investing' => $row[2],                    'financing' => $row[3],                    'free_cash_flow' => $row[4],                    'cash_flow' => $row[5],                    'net_profit' => $row[6],                    'net_profit_minus_operating' => $row[7]                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_ccc($stock_code) {            $sql_cmd = "select * from ccc('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'days_inventory_outstanding' => round($row[1], 1),                     'days_sales_outstanding' => round($row[2], 1),                     'days_payable_outstanding' => round($row[3], 1),                    'ccc' => round($row[4], 1)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_evaluation_index($stock_code) {            $sql_cmd = "select * from evaluation_index('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'inventory_index' => round($row[7], 2),                     'receivable_index' => round($row[8], 2),                     'gross_profit_index' => round($row[9], 2),                    'sga_index' => round($row[10], 2),                    'payable_index' => round($row[11], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_stock_dividend($stock_code) {            $sql_cmd = "select * from stock_dividend('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => substr($row[0], 0, 4),                     'cash_dividend' => round($row[1], 2),                     'stock_dividend_from_retained_earnings' => round($row[2], 2),                     'stock_dividend_from_capital_reserve' => round($row[3], 2),                    'stock_dividend' => round($row[4], 2),                    'total_dividend' => round($row[5], 2),                    'profit_sharing_percentage' => $row[6]                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_capital_structure_summary($stock_code) {            $sql_cmd = "select * from capital_structure_summary('$stock_code') order by activity_date";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => substr($row[0], 0, 4),                     'spo' => round($row[1], 2),                     'spo_ratio' => round($row[2], 2),                     'capitalization_earnings' => round($row[3], 2),                    'capitalization_earnings_ratio' => round($row[4], 2),                    'capitalization_reserve_and_others' => round($row[5], 2),                    'capitalization_reserve_and_others_ratio' => round($row[6], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_expected_roe_range($stock_code) {            $sql_cmd = "select * from expected_roe_range('$stock_code') order by activity_year";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'roe' => round($row[1], 2),                     'yearly_highest_price' => round($row[2], 2),                     'yearly_lowest_price' => round($row[3], 2),                    'book_value' => round($row[4], 2),                     'highest_expected_roe' => round($row[5], 2),                    'lowest_expected_roe' => round($row[6], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_expected_price_range($stock_code) {            $sql_cmd = "select * from expected_price_range('$stock_code')";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'highest_expected_price' => round($row[0], 2),                     'lowest_expected_price' => round($row[1], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        public function query_historical_prices($stock_code) {            $sql_cmd = "select activity_date, close, adj_close from HistoricalPrices where stock_code = '$stock_code'";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'date' => $row[0],                     'close' => round($row[1], 2),                     'adj_close' => round($row[2], 2)                );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }                public function query_stocktotal_dashboard() {            $sql_cmd = "select * from stocktotaldashboard";             $query = pg_query($this->conn, $sql_cmd) or die("Could not execute query: $sql_cmd");            $rv = array();            while ($row = pg_fetch_row($query)) {                $record = array(                    'stock_code' => $row[0],                     'expected_roe' => round($row[1], 2),                     'date' => $row[2],                    'income_growth' => $row[3],                    'bad_equity_ratio' => $row[4],                    'bad_equity_ratio_percentage' => round($row[5], 2),                     'bad_current_ratio' => $row[6],                    'bad_current_ratio_percentage' => round($row[7], 2),                     'bad_rapid_ratio'  => $row[8],                    'bad_rapid_ratio_percentage' => round($row[9], 2),                     'bad_dividend' => $row[10],                    'bad_dividend_percentage' => round($row[11], 2),                 );                $rv[] = $record;            }            pg_free_result($query);            return $rv;        }        private $conn_str = "host=127.0.0.1 port=5432 dbname=stocktotal user=stocktotal password=stocktotal";        private $conn;    }?>