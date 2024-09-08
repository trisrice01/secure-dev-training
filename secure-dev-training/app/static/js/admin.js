async function update_login_code(new_login_code) {
    let responseJson;
    try {
        const res = await fetch("/admin/change-login-code", {
            "method": "POST",
            "body": JSON.stringify({
                "login_code": new_login_code
            }),
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        });
        responseJson = await res.json();
    }
    catch {
        alert("Fetch failed!");
    return;r
    }

    if (!responseJson.success || responseJson.error) {
        alert(responseJson.message);
        return;
    }

    let curr = document.getElementById("current-login-code");
    curr.innerText = new_login_code
    return true;
}



(function() {
    const newCodeForm = document.getElementById("submit-new-login-code");
    newCodeForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        login_code = fd.get("login_code");
        update_login_code(login_code);
    });
    console.log(document.querySelectorAll("button[data-role=\"delete-user-btn\"]"))

})()