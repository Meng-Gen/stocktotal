<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['profit_margin']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Profit Margin Analysis");

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
        graph1.valueField = "gross_profit_margin";
        graph1.title = "Gross Profit Margin";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis; 
        graph2.valueField = "operating_profit_margin";
        graph2.title = "Operating Profit Margin";
        graph2.bullet = "triangleUp";
        graph2.hideBulletsCount = 30;
        chart.addGraph(graph2);

        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = valueAxis; 
        graph3.valueField = "net_profit_margin";
        graph3.title = "Net Profit Margin";
        graph3.bullet = "square";
        graph3.hideBulletsCount = 30;
        graph3.lineAlpha = 1;
        graph3.fillAlphas = 0.1;
        chart.addGraph(graph3);

        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);

        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("profit_margin_chart_div");
    });
</script>