<?php

//--beginning-of-vulnerable-snippet
// The GetPingCommand function is being called to create the command which will be executed.
// With the intention of triggering a ping request. It currently is vulnerable to command
// injection.
// A command that will execute a ping must be returned from this function.
// But you are free to add additional functions if needed.
function GetPingCommand($host) {
    $commandToExecute = "ping -c 4 $host";
    return $commandToExecute;
}
//--end-of-vulnerable-snippet

?>