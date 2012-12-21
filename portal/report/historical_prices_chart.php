<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['historical_prices']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Historical Prices");

        var categoryAxis = chart.categoryAxis;
        categoryAxis.parseDates = true;
        categoryAxis.minPeriod = "DD";
        categoryAxis.dashLength = 2;
        categoryAxis.gridAlpha = 0.15;
        categoryAxis.axisColor = "#DADADA";

        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.axisThickness = 2;
        valueAxis.gridAlpha = 0;
        chart.addValueAxis(valueAxis);

        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = valueAxis;
        graph1.valueField = "close";
        graph1.title = "Close";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis; 
        graph2.valueField = "adj_close";
        graph2.title = "Adj. Close";
        graph2.bullet = "triangleUp";
        graph2.hideBulletsCount = 30;
        chart.addGraph(graph2);

        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);

        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("historical_prices_chart_div");
    });
</script>