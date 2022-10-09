function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}

function send_reset_password_email()  {
    let member_email = document.getElementById("member_email").value;
    let api_url = "../user/send_reset_password_email";
    let data = { 'member_email': member_email };
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'POST',
        headers: new Headers({
            'Content-Type': "application/json"
        }),
        body: JSON.stringify(data)
    }).then(function (promise_result) {
        return promise_result.json();
    }).then(function (response) {
        console.log('yo')
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
    }).catch(function(err) {
        console.log(err);
    });
}
