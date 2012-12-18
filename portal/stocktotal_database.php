<?php
    include 'stocktotal_postgres.php';
    
    class StocktotalDatabase {
    
        public function __construct($db_type) {
            if ((strcasecmp($db_type, "postgres") == 0) or (strcasecmp($db_type, "postgresql") == 0)) {
                $this->db_impl = new StocktotalPostgres;
            } 
            else {
                throw new Exception('Please add support for your database type');
            }
        }

        public function __destruct() {
            $this->db_impl->__destruct();
        }

        public function query_roe($stock_code) {
            return $this->db_impl->query_roe($stock_code);
        }
        
        public function query_financial_structure($stock_code) {
            return $this->db_impl->query_financial_structure($stock_code);
        }
        
        private $db_impl;
    }
?>