<?php
// Dummy Blog Post Data
$title = "How to Start Learning PHP";
$date = date("F j, Y"); // current date
$author = "John Doe";
$content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce id ipsum eget magna fermentum auctor. 
Curabitur vehicula ex vel nulla vulputate, et sagittis elit ultrices. Integer consectetur venenatis mi, 
ac fermentum ligula scelerisque et. Donec mattis enim in mauris tincidunt, at vehicula lectus viverra. 
Nulla facilisi. Cras interdum, nunc ut ultricies mollis, sapien arcu consectetur orci, at faucibus erat 
sapien eget est.";

// Generate and display blog post
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $title; ?> - Blog Post</title>
    <?php 
    require("problem.php");
    if (isset($_GET["theme"]))
    {
        $theme = SanitiseTheme($_GET["theme"]);
        if ($theme == "") {
            require_once("themes/dark.php");
        } else {
            require_once($theme);
        }
    }
    else {
        require_once("themes/dark.php");
    }
    ?>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; }
        .blog-container { max-width: 800px; margin: 20px auto; padding: 20px; border: 1px solid #ddd }
        .blog-title { font-size: 28px; font-weight: bold; color: #333; }
        .blog-meta { font-size: 14px; color: #666; margin-bottom: 20px; }
        .blog-content { font-size: 18px; color: #444; }
    </style>
</head>
<body>

<div class="blog-container">
    <h1 class="blog-title"><?php echo $title; ?></h1>
    <p class="blog-meta">By <?php echo $author; ?> | <?php echo $date; ?></p>
    <div class="blog-content">
        <p><?php echo $content; ?></p>
    </div>
</div>

</body>
</html>