<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['operating_income']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Moving Average Analysis");

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
        graph1.valueField = "ma3_income";
        graph1.title = "MA3";
        graph1.lineThickness = 2;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis; 
        graph2.valueField = "ma12_income";
        graph2.title = "MA12";
        graph2.lineThickness = 2;
        chart.addGraph(graph2);

        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = valueAxis;
        graph3.valueField = "income";
        graph3.title = "Operating Income";
        graph3.type = "column";
        graph3.hidden = true; 
        chart.addGraph(graph3);

        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);

        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("operating_income_ma_chart_div");
    });
</script>