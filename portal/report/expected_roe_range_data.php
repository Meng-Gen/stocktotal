<script type="text/javascript">
    $(document).ready(function() {
        $('#expected_roe_range_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="expected_roe_range_data_private"></table>' );
        $('#expected_roe_range_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['expected_roe_range'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "ROE", "sClass": "center" },
                { "sTitle": "High", "sClass": "center" },
                { "sTitle": "Low", "sClass": "center" },
                { "sTitle": "Book Value", "sClass": "center" },
                { "sTitle": "High Expected ROE", "sClass": "center" },
                { "sTitle": "Low Expected ROE", "sClass": "center" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>