<?php
    include 'stocktotal_postgres.php';

    class StocktotalDatabase {

        public function __construct($db_type) {
            if ((strcasecmp($db_type, 'postgres') == 0) or (strcasecmp($db_type, 'postgresql') == 0)) {
                $this->db_private = new StocktotalPostgres;
            } 
            else {
                echo "Please add support for your database type";
            }
        }

        public function __destruct() {
            $this->db_private->__destruct();
        }

        public function query_roe($stock_code) {
            return $this->db_private->query_roe($stock_code);
        }

        public function query_financial_structure($stock_code) {
            return $this->db_private->query_financial_structure($stock_code);
        }

        public function query_current_and_rapid_ratio($stock_code) {
            return $this->db_private->query_current_and_rapid_ratio($stock_code);
        }

        public function query_nonoperating_income($stock_code) {
            return $this->db_private->query_nonoperating_income($stock_code);
        }

        public function query_long_term_investments($stock_code) {
            return $this->db_private->query_long_term_investments($stock_code);
        }

        public function query_operating_income($stock_code) {
            return $this->db_private->query_operating_income($stock_code);
        }

        public function query_accumlated_income_yoy($stock_code) {
            return $this->db_private->query_accumlated_income_yoy($stock_code);
        }

        public function query_profit_margin($stock_code) {
            return $this->db_private->query_profit_margin($stock_code);
        }

        public function query_cash_flow($stock_code) {
            return $this->db_private->query_cash_flow($stock_code);
        }

        public function query_ccc($stock_code) {
            return $this->db_private->query_ccc($stock_code);
        }

        public function query_evaluation_index($stock_code) {
            return $this->db_private->query_evaluation_index($stock_code);
        }

        public function query_stock_dividend($stock_code) {
            return $this->db_private->query_stock_dividend($stock_code);
        }

        public function query_capital_structure_summary($stock_code) {
            return $this->db_private->query_capital_structure_summary($stock_code);
        }

        public function query_expected_roe_range($stock_code) {
            return $this->db_private->query_expected_roe_range($stock_code);
        }

        public function query_expected_price_range($stock_code) {
            return $this->db_private->query_expected_price_range($stock_code);
        }

        public function query_historical_prices($stock_code) {
            return $this->db_private->query_historical_prices($stock_code);
        }

        public function query_stocktotal_dashboard() {
            return $this->db_private->query_stocktotal_dashboard();
        }
        
        private $db_private;

    }
?>