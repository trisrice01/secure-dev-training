<?php

require_once("problem.php");

// Only files in the themes folder should be allowed
$themesFolderPath = getcwd() . "/themes";

function VerifyPathTraversal() {
    global $themesFolderPath;
    $themePayloads = [
        ["name" => "Accessing file outside of themes folder", "path" => "../../../../etc/passwd", "expected" => ""], 
        ["name" => "Accessing expected theme file", "path" => "dark.php", "expected" => "$themesFolderPath/dark.php", "expectedTwo" => "themes/dark.php"], 
        ["name" => "Accessing invalid theme file", "path" => "red.php", "expected" => ""], 
        ["name" => "Accessing REDACTED theme file", "path" => "colourful-theme-that-no-one-knows-about.php", "expected" => "$themesFolderPath/colourful-theme-that-no-one-knows-about.php", "expectedTwo" => "themes/colourful-theme-that-no-one-knows-about.php"], 
        ["name" => "Recursion check", "path" => "....//....//....//....//etc/passwd", "expected" => ""]];
    $testResult = array();
    foreach ($themePayloads as $payload) {
        $output = SanitiseTheme($payload["path"]);
        $payloadPassed = $output == $payload["expected"];
        if (isset($payload["expectedTwo"]))
        {
            $payloadPassed = $payloadPassed || ($output == $payload["expectedTwo"]);
        }
        array_push($testResult, ["name" => $payload["name"], "passed" => $payloadPassed]);
    }
    return $testResult;
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $testResult = VerifyPathTraversal();
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($testResult);
}