<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['capital_structure_summary']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Capital Structure Summary");

        var categoryAxis = chart.categoryAxis;
        categoryAxis.parseDates = true;
        categoryAxis.minPeriod = "DD";
        categoryAxis.dashLength = 2;
        categoryAxis.gridAlpha = 0.15;
        categoryAxis.axisColor = "#DADADA";

        var valueAxis = new AmCharts.ValueAxis();
        valueAxis.title = "percent"; // this line makes the chart "stacked"
        valueAxis.stackType = "100%";
        valueAxis.gridAlpha = 0.07;
        chart.addValueAxis(valueAxis);

        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = valueAxis;
        graph1.valueField = "spo";
        graph1.title = "SPO";
        graph1.balloonText = "[[value]] ([[percents]]%)";
        graph1.lineAlpha = 0;
        graph1.fillAlphas = 0.6;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis; 
        graph2.valueField = "capitalization_earnings";
        graph2.title = "Cap. Earnings";
        graph2.balloonText = "[[value]] ([[percents]]%)";
        graph2.lineAlpha = 0;
        graph2.fillAlphas = 0.6;
        chart.addGraph(graph2);

        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = valueAxis; 
        graph3.valueField = "capitalization_reserve_and_others";
        graph3.title = "Cap. Reserve and Others";
        graph3.balloonText = "[[value]] ([[percents]]%)";
        graph3.lineAlpha = 0;
        graph3.fillAlphas = 0.6;
        chart.addGraph(graph3);

        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);

        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("capital_structure_summary_chart_div");
    });
</script>