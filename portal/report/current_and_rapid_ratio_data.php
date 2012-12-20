<script type="text/javascript">
    $(document).ready(function() {
        $('#current_and_rapid_ratio_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="current_and_rapid_ratio_data_private"></table>' );
        $('#current_and_rapid_ratio_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['current_and_rapid_ratio'])); ?>,
            "aoColumns": [
                { "sTitle": "Date", "sClass": "center", "sWidth": "30%" },
                { "sTitle": "Current Ratio", "sClass": "center", "sWidth": "40%" },
                { "sTitle": "Rapid Ratio", "sClass": "center", "sWidth": "40%" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );	
    } );
</script>