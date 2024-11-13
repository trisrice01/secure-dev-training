<?php

require_once("problem.php");


function VerifyPingWorks() {
    $payload = "127.0.0.1";

    $command = GetPingCommand($payload);

    $expected_command = "ping -c 4 '$payload'";

    $testPassed = $command == $expected_command;
    return $testPassed;
}

function VerifyPingWithId() {
    $operators = ["||", "&&", "&", ";"];
    $testPassed = true;
    foreach ($operators as $op) {
        $payload = "127.0.0.1 $op ls";
        $command = GetPingCommand($payload);
        $expected_command = "ping -c 4 '$payload'";
        if ($command != $expected_command)
        {
            $testPassed = false;
            break;
        }
    }
    return $testPassed;
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $testPassed = VerifyPingWorks() && VerifyPingWithId();
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(["passed" => $testPassed]);
}