<?php
//--beginning-of-vulnerable-snippet
// The SanitiseTheme function is being called to ensure we're protected against LFI vulnerabilities.
// Only files that exist inside the themes folder are allowed.
// Your path must be returned from the SanitiseTheme folder.
// But you are free to add additional functions if needed.
function SanitiseTheme($themeSupplied) {
    $sanitisedTheme = "themes/$themeSupplied";
    return $sanitisedTheme;
}
//--end-of-vulnerable-snippet
?>
