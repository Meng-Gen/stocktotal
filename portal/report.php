<html>
<head>
    <title>Stocktotal Report Portal</title>

    <center>
    <form action="report.php" method="post">
        <input type="text" name="stock_code" value="" />
        <input type="submit" name="submit" value="Submit" />
    </form>
    </center>

    <script src="./thirdparty/amcharts_2.8.2/amcharts/amcharts.js" type="text/javascript"></script>     
    <?php
        include 'stocktotal_database.php';
        include 'amchart_glue.php';
        
        $stock_code = (empty($_POST['stock_code'])) ? '1101' : $_POST['stock_code']; 
        if (!ctype_digit($stock_code)) {
            return;
        }
        $db = new StocktotalDatabase('postgres');
        $roe_dataset = $db->query_roe($stock_code);
        $financial_structure_dataset = $db->query_financial_structure($stock_code);

        include 'roe_report.php'; 
        include 'financial_structure_report.php';
    ?>
</head>
<body>
    <center>
    <h1>°]³ø¤ÀªR: <?php echo $stock_code; ?></h1>
    <p>
    <div id="roe_report_div" style="width:600px; height:400px;"></div>
    <p>
    <div id="financial_structure_report_div" style="width:600px; height:400px;"></div>
    </center>
</body>
</html>