<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['accumlated_income_yoy']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Accumlated Income YoY Analysis");

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

        var guide1 = new AmCharts.Guide();
        guide1.value = 0;
        guide1.dashLength = 4;
        guide1.inside = true;
        guide1.lineAlpha = 1;
        valueAxis.addGuide(guide1);

        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = valueAxis; 
        graph1.valueField = "accumlated_income_yoy";
        graph1.title = "Acc. YoY";
        graph1.lineThickness = 2;
        graph1.type = "column";
        chart.addGraph(graph1);

        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);

        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("operating_income_acc_yoy_chart_div");
    });
</script>