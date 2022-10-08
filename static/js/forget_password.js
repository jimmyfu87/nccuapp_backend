function toggleLoading(show) {
    document.querySelector('.loading').style.display =	show ? 'block' : 'none';
}

function send_reset_password_email() {
    let member_email = document.getElementById("member_email").value;
    let api_url = "../user/send_reset_password_email";
    let data = {'member_email': member_email};
    let param = JSON.stringify(data)
    let request = new XMLHttpRequest();
    request.open("POST", api_url, true);
    toggleLoading(true);
    $('#spinner-div').show();
    request.setRequestHeader("Content-Type", "application/json");
    request.send(param);
    console.log(request)
    request.onload = function() {
        response = JSON.parse(request.responseText);
        console.log(response)
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
    }
}
