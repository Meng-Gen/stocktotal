<script type="text/javascript">
    $(document).ready(function() {
        $('#operating_income_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="operating_income_data_private"></table>' );
        $('#operating_income_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['operating_income'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "Income", "sClass": "center" },
                { "sTitle": "Income YoY", "sClass": "center" },
                { "sTitle": "Acc. Income", "sClass": "center" },
                { "sTitle": "Acc. Income YoY", "sClass": "center" },                               
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>