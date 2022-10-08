function toggleLoading(show) {
    document.querySelector('.loading').style.display =	show ? 'block' : 'none';
}

function reset_password() {
    let member_new_password = document.getElementById("member_new_password").value;
    let member_new_password2 = document.getElementById("member_new_password2").value;
    if (member_new_password != member_new_password2){
        alert('Two Passwords are not the same, please confirm again');
    }
    else{
        let api_url = "../user/reset_password";
        let data = {'member_new_password': member_new_password};
        let param = JSON.stringify(data)
        let request = new XMLHttpRequest();
        request.open("PATCH", api_url, true);
        toggleLoading(true);
        $('#spinner-div').show();
        request.setRequestHeader("Content-Type", "application/json");
        request.send(param);
        console.log(request)
        request.onload = function() {
            response = JSON.parse(request.responseText);
            if (response["success"] == true) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
                window.location = '../user/Login.html';
            } else if (response["success"] == false) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
            }
        }
    }


}
