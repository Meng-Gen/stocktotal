<script type="text/javascript">
    $(document).ready(function() {
        $('#ccc_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="ccc_data_private"></table>' );
        $('#ccc_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['ccc'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "DIO", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "DSO", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "DPO", "sClass": "center", "sWidth": "20%" },
                { "sTitle": "CCC", "sClass": "center", "sWidth": "20%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>