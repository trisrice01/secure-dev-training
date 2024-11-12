<?php

if ($_SERVER["REQUEST_METHOD"] != "GET")
{
    http_response_code(400);
    die("Invalid request method.");
}

$parameter = $_GET["query"];

if (!isset($_GET["query"])) {
    http_response_code(400);
    die("Query missing from request.");
}

$conn = mysqli_connect(
    'db', # service name
    getenv('MYSQL_USER'), # username
    getenv('MYSQL_PASSWORD'), # password
    getenv('MYSQL_DATABASE') # db table
);

$table_name = "users";

//--beginning-of-vulnerable-snippet
$query = "SELECT * FROM $table_name WHERE user_id = $parameter";
$statement = $conn->query($query);
$result = $statement->fetch_all(MYSQLI_ASSOC);
//--end-of-vulnerable-snippet


// Return data to user
header('Content-Type: application/json; charset=utf-8');
echo json_encode($result);

?>