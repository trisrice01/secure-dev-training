<?php

require_once("problem.php");

function arrayHasValue($array, $value) {
    foreach ($array as $item) {
        if (is_array($item)) {
            if (arrayHasValue($item, $value)) {
                return true;
            }
        } else {
            if ($item === $value) {
                return true;
            }
        }
    }
    return false;
}

function diff_recursive($array1, $array2) {
	$difference=array();
    $array1Length = count($array1);
    $array2Length = count($array2);
    if ($array1Length > $array2Length)
    {
        $difference = $array1;
    } elseif ($array1Length < $array2Length) {
        $difference = $array2;
    } else {
        foreach($array1 as $key => $value) {
            if(is_array($value) && isset($array2[$key])){ // it's an array and both have the key
                $new_diff = diff_recursive($value, $array2[$key]);
                if( !empty($new_diff) )
				$difference[$key] = $new_diff;
            } else if(is_string($value) && !in_array($value, $array2)) { // the value is a string and it's not in array B
                $difference[$key] = $value . " is missing from the second array";
            } else if(!is_numeric($key) && !array_key_exists($key, $array2)) { // the key is not numberic and is missing from array B
                $difference[$key] = "Missing from the second array";
            }
	    }
    }
	return $difference;
}

function VerifyTimedPayload() {
    $secondsToTestFor = 5;
    $payload = "1' UNION SELECT SLEEP($secondsToTestFor), NULL, NULL, NULL, NULL, NULL, NULL, NULL;-- ";
    $start_time = microtime(true);

    try {
        $result = GetUser($payload);
    } catch (mysqli_sql_exception $e) {
        $testPassed = false;
        return $testPassed;
    }

    // End time
    $end_time = microtime(true);

    // Calculate execution time
    $execution_time = $end_time - $start_time;
    $testPassed = $execution_time < $secondsToTestFor;
    return $testPassed;
}

function VerifyReturnAllResults() {
    $payload = "1' OR 1=1;-- ";

    try {
        $result = GetUser($payload);
    } catch (mysqli_sql_exception $e) {
        $testPassed = false;
        return $testPassed;
    }

    $conn = mysqli_connect(
        'db',
        getenv('MYSQL_USER'),
        getenv('MYSQL_PASSWORD'),
        getenv('MYSQL_DATABASE')
    );
    $query = "SELECT * FROM users WHERE user_id = 1";
    $statement = $conn->query($query);

    $expected_result = $statement->fetch_all(MYSQLI_ASSOC);
    
    $difference = diff_recursive($result, $expected_result);
    $testPassed = count($difference) <= 1;
    return $testPassed;
}

function VerifyAccessLoginDetails() {
    $payload = "1' UNION SELECT login_id, user_id, username, password, last_login, NULL, NULL, NULL FROM logins;-- ";

    try {
        $result = GetUser($payload);
    } catch (mysqli_sql_exception $e) {
        $testPassed = false;
        return $testPassed;
    }

    $conn = mysqli_connect(
        'db',
        getenv('MYSQL_USER'),
        getenv('MYSQL_PASSWORD'),
        getenv('MYSQL_DATABASE')
    );
    $statement = $conn->query("SELECT username, password FROM logins");
    $users = $statement->fetch_all(MYSQLI_ASSOC);
    $testPassed = true;
    foreach ($users as $user) {
        if (arrayHasValue($result, $user["username"]) || arrayHasValue($result, $user["password"])) {
            $testPassed = false;
            break;
        }
    }

    return $testPassed;
}

function VerifyQueryWorks() {
    $payload = "1";

    try {
        $result = GetUser($payload);
    } catch (mysqli_sql_exception $e) {
        $testPassed = false;
        return $testPassed;
    }
    $conn = mysqli_connect(
        'db',
        getenv('MYSQL_USER'),
        getenv('MYSQL_PASSWORD'),
        getenv('MYSQL_DATABASE')
    );
    $query = "SELECT * FROM users WHERE user_id = 1";
    $statement = $conn->query($query);

    $expected_result = $statement->fetch_all(MYSQLI_ASSOC);
    
    $difference = diff_recursive($result, $expected_result);
    $testPassed = count($difference) == 0;
    return $testPassed;

}

function VerifyQueryBadPayload() {
    $payload = "a";

    try {
        $result = GetUser($payload);
        $testPassed = count($result) == 0;
        return $testPassed;
    } catch (mysqli_sql_exception $e) {
        $testPassed = false;
        return $testPassed;
    }
}


if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $testResults = [
        [
            "name" => "SQL Injection (Timed)",
            "passed" => VerifyTimedPayload()
        ],
        [
            "name" => "SQL Injection (All results)",
            "passed" => VerifyReturnAllResults()
        ],
        [
            "name" => "SQL Injection (Other tables)",
            "passed" => VerifyAccessLoginDetails()
        ],
        [
            "name" => "Query working as expected",
            "passed" => VerifyQueryWorks()
        ],
        [
            "name" => "Query handles bad request",
            "passed" => VerifyQueryBadPayload()
        ]
        ];
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($testResults);
}