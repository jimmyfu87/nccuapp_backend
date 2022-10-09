function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}


function register() {
    let member_id = document.getElementById('member_id').value;
    let member_password = document.getElementById("member_password").value;
    let member_email = document.getElementById("member_email").value;
    let api_url = "../user/register";
    let data = { 'member_id': member_id, 'member_password': member_password, 'member_email': member_email };
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
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message'])
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
