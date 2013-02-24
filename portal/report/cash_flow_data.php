<script type="text/javascript">
    $(document).ready(function() {
        $('#cash_flow_data_div').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="cash_flow_data_private"></table>' );
        $('#cash_flow_data_private').dataTable( {
            "aaData": <?php echo(datatables_encode($dataset['cash_flow'])); ?>,
            "aoColumns": [
                { "sTitle": "&nbsp&nbsp&nbspDate&nbsp&nbsp&nbsp", "sClass": "center" },
                { "sTitle": "Operating Activity", "sClass": "center" },
                { "sTitle": "Investing Activity", "sClass": "center" },
                { "sTitle": "Financing Activity", "sClass": "center" },
                { "sTitle": "Free Cash Flow", "sClass": "center" },
                { "sTitle": "Cash Flow", "sClass": "center" },
                { "sTitle": "Net Profit", "sClass": "center" },
                { "sTitle": "Operating Minus Net Profit", "sClass": "center" },
            ],
            "bFilter": false,
            "aaSorting": [ [0,'desc'], ],
        } );
    } );
</script>