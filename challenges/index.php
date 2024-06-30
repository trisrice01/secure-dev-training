<?php
function handle_form() {
	if ($_SERVER["REQUEST_METHOD"] !== "POST") {
		return;
	}

	if (!isset($_POST["backupname"]) || empty($_POST["backupname"])) {
		return;
	}

	$backupname = $_POST["backupname"];
	$backup_destination = "backups/{$backupname}.tar";
	passthru("tar cf {$backup_destination} index.php;");
	
	echo "backup successful!";
	echo "backup can be found at <a href=\"/{$backup_destination}\">{$backupname}.tar</a>";

}
?>
<!DOCTYPE html>

<html lang="en">
<head>
<title>Cooky industries</title>
</head>

<body>
<h1>Backup creator</h1>

<p>Create a backup of this website's source code</p>

<form method="POST" action="">
<label for="backup-name">Backup name:</label>
<input type="text" name="backupname" id="backup-name" />	
</form>

<?php

handle_form();

?>
</body>
</html>

