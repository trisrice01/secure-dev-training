<?php
function GetPingCommand($host) {
//--beginning-of-vulnerable-snippet
$commandToExecute = "ping -c 4 $host";
//--end-of-vulnerable-snippet
    return $commandToExecute;
}
?>