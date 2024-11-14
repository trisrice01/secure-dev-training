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

//--beginning-of-vulnerable-snippet
// The ConstructHTMLForNotes function is being called to create a <tr> element for a table.
// It is currently causing Cross-Site Scripting.
// A <tr> element must be returned from the function.
// But you are free to add additional functions if needed.
function ConstructHTMLForNotes($notes) {
    $html = "";
    foreach ($notes as $note) {
        $html .= "<tr>
        <td>{$note['id']}</td>
        <td>{$note['title']}</td>
        <td>{$note['description']}</td>
        </tr>";
    }
    return $html;
}
//--end-of-vulnerable-snippet

?>