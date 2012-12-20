<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['ccc']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Cash Conversion Cycle Analysis");
       
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
       
        var graph1 = new AmCharts.AmGraph();
        graph1.valueAxis = primaryValueAxis;
        graph1.valueField = "days_inventory_outstanding";
        graph1.title = "Days Inventory Outstanding";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = primaryValueAxis; 
        graph2.valueField = "days_sales_outstanding";
        graph2.title = "Days Sales Outstanding";
        graph2.bullet = "triangleUp";
        graph2.hideBulletsCount = 30;
        chart.addGraph(graph2);

        var graph3 = new AmCharts.AmGraph();
        graph3.valueAxis = primaryValueAxis; 
        graph3.valueField = "days_payable_outstanding";
        graph3.title = "Days Payable Outstanding";
        graph3.bullet = "triangleDown";
        graph3.hideBulletsCount = 30;
        chart.addGraph(graph3);
        
        var graph4 = new AmCharts.AmGraph();
        graph4.valueAxis = secondaryValueAxis;
        graph4.valueField = "ccc";
        graph4.title = "Cash Conversion Cycle";
        graph4.bullet = "square";
        graph4.hideBulletsCount = 30;
        graph4.lineAlpha = 1;
        graph4.fillAlphas = 0.1;
        chart.addGraph(graph4);
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("ccc_chart_div");
    });
</script>
