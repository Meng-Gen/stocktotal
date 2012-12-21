<script type="text/javascript">
    $(document).ready(function() {
        $('#profit_margin_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="profit_margin_data_private"></table>' );
        $('#profit_margin_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['profit_margin'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Gross Profit Margin", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Operating Profit Margin", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Net Profit Margin", "sClass": "center", "sWidth": "25%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>