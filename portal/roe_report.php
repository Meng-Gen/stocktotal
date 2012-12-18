<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.pathToImages = "./thirdparty/amcharts_2.8.2/amcharts/images/";
        chart.dataProvider = <?php echo convert_to_chartdata($roe_dataset); ?>;
        chart.categoryField = "date";
        chart.addTitle("ROE Analysis");
       
        var categoryAxis = chart.categoryAxis;
        categoryAxis.parseDates = true;
        categoryAxis.minPeriod = "DD";
        categoryAxis.dashLength = 2;
        categoryAxis.gridAlpha = 0.15;
        
        categoryAxis.axisColor = "#DADADA";

        var primaryValueAxis = new AmCharts.ValueAxis();
        primaryValueAxis.axisThickness = 2;
        primaryValueAxis.gridAlpha = 0;
        chart.addValueAxis(primaryValueAxis);

        var secondaryValueAxis = new AmCharts.ValueAxis();
        secondaryValueAxis.position = "right";
        secondaryValueAxis.gridAlpha = 0;
        secondaryValueAxis.axisThickness = 2;
        chart.addValueAxis(secondaryValueAxis);
       
        // roe graph
        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = primaryValueAxis;
        graph1.valueField = "roe";
        graph1.title = "ROE";
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
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("roe_report_div");
    });
</script>   