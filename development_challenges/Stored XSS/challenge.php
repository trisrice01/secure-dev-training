<?php
require_once("problem.php");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Note Tracker</title>
</head>
<body>
    <h1>Note Tracker</h1>
    <table border="1">
        <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Description</th>
        </tr>
        <?php echo ConstructHTMLForNotes(GetAllNotes()) ?>
    </table>
</body>
</html>
