<?php

require_once("problem.php");

function ConvertToSingleLineString($multiLineString) {
    $multiLineString = str_replace(" ", "", $multiLineString);
    $multiLineString = str_replace("\n", "", $multiLineString);
    $multiLineString = str_replace("\r", "", $multiLineString);
    return $multiLineString;
}

function TestCase($payload, $expectedResult) {
    $notesForTest = [["id" => 1, "title" => $payload, "description" => $payload]];
    $htmlToTest = ConstructHTMLForNotes($notesForTest);
    $htmlToTest = ConvertToSingleLineString($htmlToTest);
    return ($htmlToTest == $expectedResult); 
}

function VerifySpecialCharacters() {
    $payload = "<script>print()</script>";
    $expectedResult = "<tr><td>1</td><td>&lt;script&gt;print()&lt;/script&gt;</td><td>&lt;script&gt;print()&lt;/script&gt;</td></tr>";
    $testPassed = TestCase($payload, $expectedResult);
    return $testPassed;
}

function VerifyHTMLInjection() {
    $payload = "<h3>XSS</h3>";
    $expectedResult = "<tr><td>1</td><td>&lt;h3&gt;XSS&lt;/h3&gt;</td><td>&lt;h3&gt;XSS&lt;/h3&gt;</td></tr>";
    $testPassed = TestCase($payload, $expectedResult);
    return $testPassed;
}

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $testResults = [
        [
            "name" => "XSS",
            "passed" => VerifySpecialCharacters()
        ],
        [
            "name" => "HTML Injection",
            "passed" => VerifyHTMLInjection()
        ],
        ];
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode($testResults);
}