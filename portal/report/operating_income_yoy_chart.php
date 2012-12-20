<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['operating_income']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Income YoY Analysis");
       
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
        secondaryValueAxis.axisThickness = 2;
        secondaryValueAxis.gridAlpha = 0;
        chart.addValueAxis(secondaryValueAxis);
        
        var guide1 = new AmCharts.Guide();
        guide1.value = 0;
        guide1.dashLength = 4;
        guide1.inside = true;
        guide1.lineAlpha = 2;
        primaryValueAxis.addGuide(guide1);
        
        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = secondaryValueAxis; 
        graph1.valueField = "income_yoy";
        graph1.title = "YoY";
        graph1.lineThickness = 2;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = primaryValueAxis;
        graph2.valueField = "income";
        graph2.title = "Operating Income";
        graph2.type = "column";
        chart.addGraph(graph2);
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("operating_income_yoy_chart_div");
    });
</script>   