<html>

<head>
    <title>Stocktotal Report Portal</title>

    <form action="report.php" method="post">
        <input type="text" name="stock_code" value="" />
        <input type="submit" name="submit" value="Submit" />
    </form>
    
    <?php
        // get chartdata from database
        $stock_code = (empty($_POST['stock_code'])) ? '1101' : $_POST['stock_code']; 

        include 'stocktotal_database.php';
        $db = new StocktotalDatabase('postgres');
        $roe_dataset = $db->query_roe($stock_code);

        // convert to amchart chartdata
        include 'amchart_glue.php';
        $chartdata = convert_to_chartdata($roe_dataset);
    ?>

    <script src="./thirdparty/amcharts_2.8.2/amcharts/amcharts.js" type="text/javascript"></script>         
    <script type="text/javascript">
        var chart;
        var chartData = <?php echo $chartdata; ?>;

        AmCharts.ready(function () {
            // SERIAL CHART    
            chart = new AmCharts.AmSerialChart();
            chart.pathToImages = "./thirdparty/amcharts_2.8.2/amcharts/images/";
            chart.dataProvider = chartData;
            chart.categoryField = "date";
            chart.addTitle("ROE Analysis");
            
            // AXES
            // category                
            var categoryAxis = chart.categoryAxis;
            categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
            categoryAxis.minPeriod = "DD";
            categoryAxis.dashLength = 2;
            categoryAxis.gridAlpha = 0.15;
            
            categoryAxis.axisColor = "#DADADA";

            // first value axis (on the left)
            var primaryValueAxis = new AmCharts.ValueAxis();
            //primaryValueAxis.axisColor = "#FF6600";
            primaryValueAxis.axisThickness = 2;
            primaryValueAxis.gridAlpha = 0;
            chart.addValueAxis(primaryValueAxis);

            // second value axis (on the right) 
            var secondaryValueAxis = new AmCharts.ValueAxis();
            secondaryValueAxis.position = "right"; // this line makes the axis to appear on the right
            //secondaryValueAxis.axisColor = "#FCD202";
            secondaryValueAxis.gridAlpha = 0;
            secondaryValueAxis.axisThickness = 2;
            chart.addValueAxis(secondaryValueAxis);

            // GRAPHS
            // roe graph
            var graph1 = new AmCharts.AmGraph();
            graph1.valueAxis = primaryValueAxis;
            graph1.title = "ROE";
            graph1.valueField = "roe";
            graph1.bullet = "round";
            graph1.hideBulletsCount = 30;
            chart.addGraph(graph1);

            // net profit margin graph
            var graph2 = new AmCharts.AmGraph();
            graph2.valueAxis = primaryValueAxis; 
            graph2.valueField = "net_profit_margin";
            graph2.title = "Net Profit Margin";
            graph2.bullet = "triangleUp";
            graph2.hideBulletsCount = 30;
            chart.addGraph(graph2);

            // total assets turnover graph
            var graph3 = new AmCharts.AmGraph();
            graph3.valueAxis = primaryValueAxis; 
            graph3.valueField = "total_assets_turnover";
            graph3.title = "Total Assets Turnover";
            graph3.bullet = "triangleUp";
            graph3.hideBulletsCount = 30;
            chart.addGraph(graph3);
            
            // equity multiplier graph                
            var graph4 = new AmCharts.AmGraph();
            graph4.valueAxis = secondaryValueAxis;
            graph4.title = "Equity Multiplier";
            graph4.valueField = "equity_multiplier";
            graph4.bullet = "square";
            graph4.hideBulletsCount = 30;
            chart.addGraph(graph4);
            
            // LEGEND
            var legend = new AmCharts.AmLegend();
            legend.marginLeft = 110;
            chart.addLegend(legend);

            // WRITE
            chart.write("roe_chart_div");
        });
    </script>
</head>

<body>
    <h1>°]³ø¤ÀªR: <?php echo $stock_code; ?></h1>
    <div id="roe_chart_div" style="width:600px; height:400px;"></div>
</body>

</html>