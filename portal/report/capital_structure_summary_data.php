<script type="text/javascript">
    $(document).ready(function() {
        $('#capital_structure_summary_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="capital_structure_summary_data_private"></table>' );
        $('#capital_structure_summary_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['capital_structure_summary'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center" },
                { "sTitle": "SPO", "sClass": "center" },
                { "sTitle": "Ratio", "sClass": "center" },
                { "sTitle": "Cap. Earnings", "sClass": "center" },
                { "sTitle": "Ratio", "sClass": "center" },
                { "sTitle": "Cap. Reserve and Others", "sClass": "center" },
                { "sTitle": "Ratio", "sClass": "center" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>