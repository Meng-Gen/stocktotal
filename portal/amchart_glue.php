<?php    function convert_to_chartdata($db_dataset) {        $rv = "[";        foreach($db_dataset as $row){            $rv .= "{ ";            foreach($row as $key => $value) {                if ($key == "date") {                    $year = substr($value, 0, 4);                    $month = substr($value, 5, 2) - 1;                    $rv .= "date: new Date($year, $month, 1), ";                }                else {                    $rv .= "$key: $value, ";                }            }            $rv .= "}, ";        }        $rv .= "]";                     return $rv;    }?>