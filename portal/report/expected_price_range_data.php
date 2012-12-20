<script type="text/javascript">
    $(document).ready(function() {
        $('#expected_price_range_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="expected_price_range_data_private"></table>' );
        $('#expected_price_range_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['expected_price_range'])); ?>,
            "aoColumns": [
                { "sTitle": "Expected High (Sell)", "sClass": "center", "sWidth": "50%" },
                { "sTitle": "Expected Low (Buy)", "sClass": "center", "sWidth": "50%" },
            ],
            "bFilter": false,
            "bPaginate": false,
            "bSort": false,
            "bInfo": false,
        } );	
    } );
</script>