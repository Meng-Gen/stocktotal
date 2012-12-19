<html>
<head>
    <title>Stocktotal Report Portal</title>

    <center>
    <form action="report.php" method="post">
        <input type="text" name="stock_code" value="" />
        <input type="submit" name="submit" value="Submit" />
    </form>
    </center>

    <?php
        include 'stocktotal_database.php';
        include 'amchart_glue.php';
        
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
        
        // generate reports
        include 'roe_report.php'; 
        include 'financial_structure_report.php';
        include 'current_and_rapid_ratio_report.php';
        include 'nonoperating_income_report.php';
        include 'long_term_investments_report.php';
        include 'operating_income_report.php';
        include 'profit_margin_report.php';
        include 'ccc_report.php';
    ?>
</head>
<body>
    <center>
    <h1>
    <?php 
        echo "Stocktotal Analysis: " . $stock_code; 
        if ((strcmp($stock_code, $DEFAULT_STOCK_CODE) == 0)) {
            echo " (default)";
        }
    ?>
    </h1>
    <hr/><p/>
    <div id="roe_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="financial_structure_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="current_and_rapid_ratio_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="nonoperating_income_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="long_term_investments_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="operating_income_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="profit_margin_report_div" style="width:600px; height:400px;"></div>
    <hr/><p/>
    <div id="ccc_report_div" style="width:600px; height:400px;"></div>
    </center>
</body>
</html>