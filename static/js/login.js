function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}

function login() {
    let member_id = document.getElementById('member_id').value;
    let member_password = document.getElementById("member_password").value;
    let data = { 'member_id': member_id, 'member_password': member_password };
    let api_url = "user/login";
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
            console.log('success')
            toggleLoading(false);
            $('#spinner-div').hide();
            window.location = '../product';
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
        }
    }).catch(function(err) {
        console.log(err);
    });
}
