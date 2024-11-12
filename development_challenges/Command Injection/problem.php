<?php
function pingServer($host) {
    //--beginning-of-vulnerable-snippet
    exec("ping -c 4 $host", $output, $status);

    return $output;
    //--end-of-vulnerable-snippet
}

if (isset($_POST['host'])) {
    $host = $_POST['host'];
    $result = pingServer($host);
    echo implode("<br>", array_map('htmlspecialchars', $result));
    die();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ping a Server</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333; text-align: center; }
        form { margin-top: 20px; }
        input[type="text"] { padding: 8px; width: 300px; font-size: 16px; }
        input[type="submit"] { padding: 8px 16px; font-size: 16px; }
        .output { margin-top: 20px; white-space: pre; background: #e9e9e9; padding: 10px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Ping a Server</h1>
    <form method="post" action="">
        <input type="text" name="host" placeholder="Enter hostname or IP address" required>
        <input type="submit" value="Ping">
    </form>
</body>
</html>
