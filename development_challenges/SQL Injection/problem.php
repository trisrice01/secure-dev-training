<?php

function GetUser($userId) {
    $table_name = "users";
    $conn = mysqli_connect(
        'db', # service name
        getenv('MYSQL_USER'), # username
        getenv('MYSQL_PASSWORD'), # password
        getenv('MYSQL_DATABASE') # db table
    );
//--beginning-of-vulnerable-snippet
$query = "SELECT * FROM $table_name WHERE user_id = $userId";
$statement = $conn->query($query);
$result = $statement->fetch_all(MYSQLI_ASSOC);
//--end-of-vulnerable-snippet
    return $result;
}

?>