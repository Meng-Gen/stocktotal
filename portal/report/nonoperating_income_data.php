<script type="text/javascript">
    $(document).ready(function() {
        $('#nonoperating_income_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="nonoperating_income_data_private"></table>' );
        $('#nonoperating_income_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['nonoperating_income'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "50%" },
                { "sTitle": "Non-operating Income Ratio", "sClass": "center", "sWidth": "50%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>