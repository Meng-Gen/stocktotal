<script type="text/javascript">
    $(document).ready(function() {
        $('#evaluation_index_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="evaluation_index_data_private"></table>' );
        $('#evaluation_index_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['evaluation_index'])); ?>,
            "aoColumns": [
                { "sTitle": "&nbsp&nbsp&nbspDate&nbsp&nbsp&nbsp", "sClass": "center" },
                { "sTitle": "Inventory Index", "sClass": "center" },
                { "sTitle": "Receivable Index", "sClass": "center" },
                { "sTitle": "Gross Profit Index", "sClass": "center" },
                { "sTitle": "SGA Index", "sClass": "center" },
                { "sTitle": "Payable Index", "sClass": "center" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>