function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}

function reset_password() {
    let member_new_password = document.getElementById("member_new_password").value;
    let member_new_password2 = document.getElementById("member_new_password2").value;
    if (member_new_password != member_new_password2) {
        alert('Two Passwords are not the same, please confirm again');
    }
    else {
        let api_url = "../user/reset_password";
        let data = { 'member_new_password': member_new_password };
        toggleLoading(true);
        $('#spinner-div').show();
        fetch(api_url, {
            method: 'PATCH',
            headers: new Headers({
                'Content-Type': "application/json"
            }),
            body: JSON.stringify(data)
        }).then(function (promise_result) {
            return promise_result.json();
        }).then(function (response) {
            if (response["success"] == true) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
                window.location = '../Login.html';
            } else if (response["success"] == false) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
            }
        }).catch(function (err) {
            console.log(err);
        });
    }
}
