<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo convert_to_chartdata($dataset['nonoperating_income']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Non-operating Income Analysis");
       
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

        var graph = new AmCharts.AmGraph();
        graph.valueAxis = valueAxis;
        graph.valueField = "non_operating_income_ratio";
        graph.title = "Non-operating Income Ratio";
        graph.bullet = "round";
        graph.hideBulletsCount = 30;
        chart.addGraph(graph);
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("nonoperating_income_chart_div");
    });
</script>   