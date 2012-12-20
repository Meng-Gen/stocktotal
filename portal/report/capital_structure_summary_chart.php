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
        valueAxis.axisThickness = 2;
        valueAxis.gridAlpha = 0;
        chart.addValueAxis(valueAxis);

        var guide1 = new AmCharts.Guide();
        guide1.value = 0.5;
        guide1.dashLength = 4;
        guide1.inside = true;
        guide1.lineAlpha = 1;
        valueAxis.addGuide(guide1);
        
        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = valueAxis;
        graph1.valueField = "spo_ratio";
        graph1.title = "SPO Ratio";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis; 
        graph2.valueField = "capitalization_earnings_ratio";
        graph2.title = "Cap. Earnings Ratio";
        graph2.bullet = "triangleUp";
        graph2.hideBulletsCount = 30;
        chart.addGraph(graph2);
        
        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = valueAxis; 
        graph3.valueField = "capitalization_reserve_and_others_ratio";
        graph3.title = "Cap. Reserve and Others Ratio";
        graph3.bullet = "triangleUp";
        graph3.hideBulletsCount = 30;
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