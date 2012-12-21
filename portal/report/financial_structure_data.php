<script type="text/javascript">
    $(document).ready(function() {
        $('#financial_structure_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="financial_structure_data_private"></table>' );
        $('#financial_structure_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['financial_structure'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Equity Ratio", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Liabilities Ratio", "sClass": "center", "sWidth": "25%" },
                { "sTitle": "Equity Multiplier", "sClass": "center", "sWidth": "25%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>