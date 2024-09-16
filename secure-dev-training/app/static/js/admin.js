async function postJSON(data, endpoint) {
    const res = await fetch(endpoint, {
        "method": "POST",
        "body": JSON.stringify(data),
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    });
    return res;
}

async function update_login_code(new_login_code) {
    let responseJson;
    try {
        const res = await postJSON({login_code: new_login_code}, "/admin/change-login-code");
        responseJson = await res.json();
    }
    catch {
        alert("Fetch failed!");
        return;
    }

    if (!responseJson || !responseJson.success || responseJson.error) {
        alert(responseJson.message);
        return;
    }

    let curr = document.getElementById("current-login-code");
    curr.innerText = new_login_code
    return true;
}


async function deleteUser(target) {
    const userId = target.dataset.id;
    let responseJson;
    try {
        const res = await postJSON({"user_id": userId}, "/admin/delete-user");
        responseJson = await res.json();
    } catch {
        alert("Fetch failed!");
        return;
    }

    if (!responseJson || !responseJson.error || !responseJson.success) {
        alert(responseJson.message || "Failed!");
    }
    debugger;
    let parent = target.parentNode;
    parent.previousElementSibling.innerHTML = "N/A";
    parent.innerHTML = "";
}


(function() {
    const newCodeForm = document.getElementById("submit-new-login-code");
    newCodeForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const fd = new FormData(e.target);
        login_code = fd.get("login_code");
        update_login_code(login_code);
    });
    document.querySelectorAll("button[data-role=\"delete-user-btn\"]").forEach((btn) => {
        btn.addEventListener("click", (e) => {
            deleteUser(e.target);
        })
    })
    console.log(document.querySelectorAll("button[data-role=\"delete-user-btn\"]"))

})()