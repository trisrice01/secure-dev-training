<?php
if (!isset($_COOKIE["user"])) {
    die("You must log in first");
}

$con = mysqli_connect("147.215.12.1", "datauser", "Password123!", "accounts");

$query = htmlspecialchars($_POST["query"]);

$result = mysqli_multi_query($con,"SELECT * FROM users WHERE username='"$_COOKIE["user"]."'&&qu='".$query."'");
$row = mysqli_fetch_array($result):

if (empty($row)) {
    echo "No result<br>\n";
} else {
     echo "The result found: " + $query +"<br>\n";  
}

mysqli_close($con);
?>
