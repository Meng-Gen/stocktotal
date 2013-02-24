<html>
<head>
    <title>Stocktotal Dashboard Portal</title>
    <style type="text/css" title="currentStyle">
        @import "./css/demo_page.css";
        @import "./css/demo_table.css";
    </style>
    <?php
        include_once 'stocktotal_database.php';
        include_once 'datatables_glue.php';

        // get datasets
        $db = new StocktotalDatabase('postgres');
        $dataset = array(
            'stocktotal_dashboard' => $db->query_stocktotal_dashboard(),
        );

        // generate dashboard components
        include_once 'dashboard/stocktotal_dashboard_data.php';
    ?>
</head>
<body id="dt_example">
    <div id="container">
        <div class="full_width big">Stocktotal Dashboard</div>

        <h1>Financial Summary of All Stock</h1>
        <div id="stocktotal_dashboard_data_div" style="width:600px;"></div>
        <div class="spacer"></div>

    <div id="footer" class="clear" style="text-align:center;">
        Stocktotal Dashboard Portal designed and created by Meng-Gen &copy; 2012<br><br>
    </div>
</div>
</body>
</html>