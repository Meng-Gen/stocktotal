<script type="text/javascript">
    $(document).ready(function() {
        $('#stocktotal_dashboard_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="stocktotal_dashboard_data_private"></table>' );
        $('#stocktotal_dashboard_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['stocktotal_dashboard'])); ?>,
            "aoColumns": [
                { "sTitle": "Stock Code", "sClass": "center" },
                { "sTitle": "Expected ROE", "sClass": "center" },
                { "sTitle": "Max Income Date", "sClass": "center" },
                { "sTitle": "Income Growth", "sClass": "center" },
                { "sTitle": "# Bad Equity Ratio", "sClass": "center" },
                { "sTitle": "%", "sClass": "center" },
                { "sTitle": "# Bad Current Ratio", "sClass": "center" },
                { "sTitle": "%", "sClass": "center" },
                { "sTitle": "# Bad Rapid Ratio", "sClass": "center" },
                { "sTitle": "%", "sClass": "center" },
                { "sTitle": "# Bad Stock Dividend", "sClass": "center" },
                { "sTitle": "%", "sClass": "center" },
            ],
            "bPaginate": false,
            "aaSorting": [ [3,'desc'], ],
        } );
    } );
</script>