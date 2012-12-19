<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo convert_to_chartdata($dataset['financial_structure']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Financial Structure Analysis");
       
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
        guide1.value = 0.5;
        guide1.dashLength = 4;
        guide1.inside = true;
        guide1.lineAlpha = 1;
        primaryValueAxis.addGuide(guide1);
        
        // equity ratio graph
        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = primaryValueAxis;
        graph1.valueField = "equity_ratio";
        graph1.title = "Equity Ratio";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        chart.addGraph(graph1);

        // liabilities ratio graph
        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = primaryValueAxis; 
        graph2.valueField = "liabilities_ratio";
        graph2.title = "Liabilities Ratio";
        graph2.bullet = "triangleUp";
        graph2.hideBulletsCount = 30;
        chart.addGraph(graph2);
        
        // equity multiplier graph                
        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = secondaryValueAxis;
        graph3.valueField = "equity_multiplier";
        graph3.title = "Equity Multiplier";
        graph3.bullet = "square";
        graph3.hideBulletsCount = 30;
        chart.addGraph(graph3);
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("financial_structure_report_div");
    });
</script>   