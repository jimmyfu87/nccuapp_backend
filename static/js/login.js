function toggleLoading(show) {
    document.querySelector('.loading').style.display =	show ? 'block' : 'none';
}

function login() {
    let member_id = document.getElementById('member_id').value;
    let member_password = document.getElementById("member_password").value;
    let api_url = "user/login";
    let data = {'member_id': member_id, 'member_password': member_password };
    let param = JSON.stringify(data)
    let request = new XMLHttpRequest();
    request.open("POST", api_url, true);
    toggleLoading(true);
    $('#spinner-div').show();
    request.setRequestHeader("Content-Type", "application/json");
    request.send(param);
    request.onload = function() {
        response = JSON.parse(request.responseText);
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            window.location = '../product';
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
        }
    }
}
