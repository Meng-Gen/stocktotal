<script type="text/javascript">
    AmCharts.ready(function () {
        var chart = new AmCharts.AmSerialChart();
        chart.dataProvider = <?php echo amchart_encode($dataset['cash_flow']); ?>;
        chart.categoryField = "date";
        chart.addTitle("Cash Flow Analysis");
       
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
        graph1.valueField = "free_cash_flow";
        graph1.title = "Free Cash Flow";
        graph1.bullet = "round";
        graph1.hideBulletsCount = 30;
        //graph1.lineThickness = 3;
        graph1.lineAlpha = 1;
        graph1.fillAlphas = 0.5;
        chart.addGraph(graph1);

        var graph2 = new AmCharts.AmGraph();
        graph2.valueAxis = valueAxis;
        graph2.valueField = "net_profit_minus_operating";
        graph2.title = "Net Profit Minus Operating";
        graph2.bullet = "square";
        graph2.hideBulletsCount = 30;
        graph2.lineThickness = 2;
        graph2.lineColor = "#0D52D1";
        chart.addGraph(graph2);
        
        chartCursor = new AmCharts.ChartCursor();
        chartCursor.cursorPosition = "mouse";
        chart.addChartCursor(chartCursor);
        
        var legend = new AmCharts.AmLegend();
        legend.marginLeft = 110;
        chart.addLegend(legend);

        chart.write("cash_flow_chart_div");
    });
</script>
