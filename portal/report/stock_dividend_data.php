<script type="text/javascript">
    $(document).ready(function() {
        $('#stock_dividend_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="stock_dividend_data_private"></table>' );
        $('#stock_dividend_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['stock_dividend'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "22%" },
                { "sTitle": "Cash Dividend", "sClass": "center" },
                { "sTitle": "Stock Dividend From Retained Earnings", "sClass": "center", "sWidth": "13%" },
                { "sTitle": "Stock Dividend From Capital Reserve", "sClass": "center", "sWidth": "13%" },
                { "sTitle": "Stock Dividend", "sClass": "center", "sWidth": "13%" },
                { "sTitle": "Total Dividend", "sClass": "center", "sWidth": "13%" },
                { "sTitle": "Profit Sharing %", "sClass": "center", "sWidth": "13%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>