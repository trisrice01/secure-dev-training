<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_POST["snippet"])) {
        UpdateCodeSnippet($_POST["snippet"]);
    }
    else {
        http_response_code(400);
        die("Invalid request body.");    
    }
} 
elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
    GetCurrentCodeSnippet();
}
else {
    http_response_code(400);
    die("Invalid request method.");
}

function UpdateCodeSnippet($snippet) {
    $problemFile = file_get_contents("problem.php");
    if ($problemFile == false) {
        http_response_code(500);
        die("Failed to open code snippet");
    }
    $pattern = "/(?<=\/\/--beginning-of-vulnerable-snippet\n)[\s\S]*?(?=\/\/--end-of-vulnerable-snippet)/";
    $updatedContents = preg_replace($pattern, $snippet, $problemFile);
    if (file_put_contents("problem.php", $updatedContents) === false) {
        http_response_code(500);
        die("Failed to update code snippet.");
    } else {
        http_response_code(200);
    }
}

function GetCurrentCodeSnippet() {
    $problemFile = file_get_contents("problem.php");
    if ($problemFile == false) {
        http_response_code(500);
        die("Failed to open code snippet.");
    }
    $pattern = "/(?<=\/\/--beginning-of-vulnerable-snippet\n)[\s\S]*?(?=\/\/--end-of-vulnerable-snippet)/";
    preg_match($pattern, $problemFile, $matches);
    if (!empty($matches[0])) {
        echo $matches[0];
    } else {
        http_response_code(500);
        die("Code snippet unavailable, restart the lab.");
    }
}


?>