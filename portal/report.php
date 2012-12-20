<html>
<head>
    <title>Stocktotal Report Portal</title>
    <style type="text/css" title="currentStyle">
        @import "./css/demo_page.css";
        @import "./css/demo_table.css";
    </style>
    <?php
        include 'stocktotal_database.php';
        include 'amchart_glue.php';
        include 'datatables_glue.php';
        
        $DEFAULT_STOCK_CODE = '2330';
        
        // parse and check stock code
        $stock_code = (empty($_POST['stock_code'])) ? $DEFAULT_STOCK_CODE : $_POST['stock_code']; 
        if ((strlen($stock_code) > 10) || (!ctype_digit($stock_code))) {
            echo "<center><h1>Please input valid stock code (No SQL injection!)</h1></center>";
            return;
        }
        
        // get datasets
        $db = new StocktotalDatabase('postgres');
        $dataset = array(
            'roe'                       => $db->query_roe($stock_code),
            'financial_structure'       => $db->query_financial_structure($stock_code),
            'current_and_rapid_ratio'   => $db->query_current_and_rapid_ratio($stock_code),
            'nonoperating_income'       => $db->query_nonoperating_income($stock_code),
            'long_term_investments'     => $db->query_long_term_investments($stock_code),
            'operating_income'          => $db->query_operating_income($stock_code),
            'accumlated_income_yoy'     => $db->query_accumlated_income_yoy($stock_code),
            'profit_margin'             => $db->query_profit_margin($stock_code),
            'cash_flow'                 => $db->query_cash_flow($stock_code),
            'ccc'                       => $db->query_ccc($stock_code),
            'evaluation_index'          => $db->query_evaluation_index($stock_code),
            'stock_dividend'            => $db->query_stock_dividend($stock_code),
            'capital_structure_summary' => $db->query_capital_structure_summary($stock_code),
            'expected_roe_range'        => $db->query_expected_roe_range($stock_code),
            'expected_price_range'      => $db->query_expected_price_range($stock_code),
        );
        
        // generate report components
        include 'report/roe_chart.php'; 
        include 'report/roe_data.php'; 
        include 'report/financial_structure_chart.php';
        include 'report/financial_structure_data.php';
        include 'report/current_and_rapid_ratio_chart.php';
        include 'report/current_and_rapid_ratio_data.php';
        include 'report/nonoperating_income_chart.php';
        include 'report/nonoperating_income_data.php';
        include 'report/long_term_investments_chart.php';
        include 'report/long_term_investments_data.php';
        include 'report/operating_income_chart.php';
        include 'report/profit_margin_chart.php';
        include 'report/profit_margin_data.php';
        include 'report/cash_flow_data.php';
        include 'report/ccc_chart.php';
        include 'report/ccc_data.php';
        include 'report/evaluation_index_data.php';
        include 'report/stock_dividend_data.php';
        
        include 'report/capital_structure_summary_chart.php';
        include 'report/capital_structure_summary_data.php';
        
        include 'report/expected_roe_range_data.php';
        include 'report/expected_price_range_data.php';
    ?>
</head>
<body id="dt_example">
    <div id="container">
        <div class="full_width big">Stocktotal Analysis</div>
        
        <h1>Taiwan Stock Code (Default: <?php echo "2330"; ?>)</h1>
        <p></p>
        <form action="report.php" method="post">
            <input type="text" name="stock_code" value="" />
            <input type="submit" name="submit" value="Submit" />
        </form>
        
        <h1>ROE Analysis</h1>
        <p>
            There are three components in the calculation of ROE: the net profit margin, the asset turnover, and the equity multiplier.
        </p>
        <div id="roe_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="roe_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Financial Structure Analysis</h1>
        <p>
            The equity ratio should be larger than 50%.
        </p>
        <div id="financial_structure_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="financial_structure_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Current/Rapid Ratio Analysis</h1>
        <p>
            The current ratio should be larger than 1. 
            The rapid ratio should be larger than 2.
        </p>
        <div id="current_and_rapid_ratio_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="current_and_rapid_ratio_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Non-operating Income Analysis</h1>
        <p></p>
        <div id="nonoperating_income_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>        
        <div id="nonoperating_income_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Long-term Investments Analysis</h1>
        <p></p>
        <div id="long_term_investments_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="long_term_investments_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Operating Income Analysis</h1>
        <p></p>
        <div id="operating_income_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        
        <h1>Profit Margin Analysis</h1>
        <p></p>
        <div id="profit_margin_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="profit_margin_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Cash Flow Analysis</h1>
        <p></p>
        <div id="cash_flow_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Cash Conversion Cycle Analysis</h1>
        <p>
            The cash conversion cycle (CCC) measures how long a firm will be deprived of cash if it increases its investment in resources in order to expand customer sales.  
            It is thus a measure of the liquidity risk entailed by growth. 
        </p>
        <div id="ccc_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="ccc_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Evaluation Index Analysis</h1>
        <p></p>
        <div id="evaluation_index_data_div" style="width:600px;"></div>
        <div class="spacer"></div>

        <h1>Stock Dividend</h1>
        <p></p>
        <div id="stock_dividend_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        
        <h1>Capital Structure Summary</h1>
        <p></p>
        <div id="capital_structure_summary_chart_div" style="width:600px; height:400px;"></div>
        <div class="spacer"></div>
        <div id="capital_structure_summary_data_div" style="width:600px;"></div>
        <div class="spacer"></div>

        <h1>Investment Strategy</h1>
        <p></p>
        <div id="expected_roe_range_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
        <div id="expected_price_range_data_div" style="width:600px;"></div>
        <div class="spacer"></div>
    </div>
    
    <div id="footer" class="clear" style="text-align:center;">
        Stocktotal Report Portal designed and created by Meng-Gen &copy; 2012<br><br>
    </div>
</div>
</body>
</html>