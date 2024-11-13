<?php


function GetAllNotes() {
    $conn = mysqli_connect(
        'db',
        getenv('MYSQL_USER'),
        getenv('MYSQL_PASSWORD'),
        getenv('MYSQL_DATABASE')
    );
    $query = "SELECT * FROM tasks";
    $statement = $conn->query($query);
    $result = $statement->fetch_all(MYSQLI_ASSOC);
    return $result;
}

function ConstructHTMLForNotes($notes) {
    $html = "";
    foreach ($notes as $note) {
//--beginning-of-vulnerable-snippet
$html .= "<tr>
<td>{$note['id']}</td>
<td>{$note['title']}</td>
<td>{$note['description']}</td>
</tr>";
//--end-of-vulnerable-snippet
    }
    return $html;
}

?>