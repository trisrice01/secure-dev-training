<?php
$pageToShow = "";

if (!isset($_GET["page"]) || empty($_GET["page"])) {
	$pageToShow = "home.html";
} else {
	$pageToShow = $_GET["page"];
}

?>

<html lang="en">
	<head>
		<link rel="stylesheet" href="style.css" />
		<title>Lazy Local File Inclusion</title>
	</head>

	<body>
		<header>
			<nav>
				<a href="/?page=home.html">Home</a>
				<div class="nav-links">
					<a href="/admin/admin.html">Admin</a>
					<a href="/?page=menu.html">Menu</a>
				</div>
		</header>
		<main>
			<?php include($pageToShow); ?>
		</main>
	</body>
</html>
