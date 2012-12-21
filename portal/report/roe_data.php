<script type="text/javascript">
    $(document).ready(function() {
        $('#roe_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="roe_data_private"></table>' );
        $('#roe_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['roe'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "ROE", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "Net Profit Margin", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "Total Assets Turnover", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "Equity Multiplier", "sClass": "center", "sWidth": "20%" }
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>