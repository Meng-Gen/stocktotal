<script type="text/javascript">
    $(document).ready(function() {
        $('#long_term_investments_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="long_term_investments_data_private"></table>' );
        $('#long_term_investments_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['long_term_investments'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Long-term Investments", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Assets", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Ratio", "sClass": "center", "sWidth": "25%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>