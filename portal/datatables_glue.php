<script type="text/javascript" language="javascript" src="./lib/jquery.js"></script>
<script type="text/javascript" language="javascript" src="./lib/jquery.dataTables.js"></script>

<?php
    function datatables_encode($db_dataset) {
        $rv = "[";
        foreach($db_dataset as $row){
            $rv .= "[ ";
            foreach($row as $key => $value) {
                if ($key == "date") {
                    $date_value = substr($value, 0, 7);
                    $rv .= "\"$date_value\"";
                }
                else {
                    $rv .= "\"$value\"";
                }
                $rv .= ", ";
            }
            $rv .= "], ";
        }
        $rv .= "]";             
        return $rv;
    }
?>