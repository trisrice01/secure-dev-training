<?php

require_once("problem.php");

if ($_SERVER["REQUEST_METHOD"] != "GET")
{
    http_response_code(400);
    die("Invalid request method.");
}


if (!isset($_GET["id"])) {
    http_response_code(400);
    die("Query missing from request.");
}

$userId = $_GET["id"];

$result = GetUser($userId);

// Return data to user
header('Content-Type: application/json; charset=utf-8');
echo json_encode($result);

?>