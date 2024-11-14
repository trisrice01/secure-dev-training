<?php
$conn = mysqli_connect(
    'db', # service name
    getenv('MYSQL_USER'), # username
    getenv('MYSQL_PASSWORD'), # password
    getenv('MYSQL_DATABASE') # db table
);

//--beginning-of-vulnerable-snippet
// The GetUser function is being called to retrieve a user's information.
// It is currently vulnerable to SQL Injection.
// A user's information must be returned inside an array from the GetUser function.
// But you are free to add additional functions if needed.
function GetUser($userId) {
    global $conn;
    $query = "SELECT * FROM users WHERE user_id = '$userId'";
    $statement = $conn->query($query);
    $result = $statement->fetch_all(MYSQLI_ASSOC);
    return $result;
}
//--end-of-vulnerable-snippet

?>