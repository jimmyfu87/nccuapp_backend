function toggleLoading(show) {
    document.querySelector('.loading').style.display = show ? 'block' : 'none';
}

function logout() {
    let api_url = '../user/logout';
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'GET',
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
            window.location = '../Login.html';
        }
    }).catch(function (err) {
        console.log(err);
    });
}

function add_product_topool() {
    let product_url = document.getElementById('product_url').value;
    let data = { 'input_url': product_url };
    let api_url = "../product/add_product_topool";
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
            location.reload()
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
            location.reload()
        }
    }).catch(function (err) {
        console.log(err);
    });
}

function update_all_product() {
    let api_url = '../product/update_all_product';
    toggleLoading(true);
    $('#spinner-div').show();
    fetch(api_url, {
        method: 'PUT',
    }).then(function (promise_result) {
        return promise_result.json();
    }).then(function (response) {
        if (response["success"] == true) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
            location.reload()
        } else if (response["success"] == false) {
            toggleLoading(false);
            $('#spinner-div').hide();
            alert(response['message']);
            location.reload()
        }
    }).catch(function (err) {
        console.log(err);
    });

}
//delete button 
$(document).ready(function () {
    $("#datatable").on('click', '.btn-danger', function () {
        let currentRow = $(this).closest("tr");
        let product_id = currentRow.attr('id')
        // let product_name = currentRow.find("th:eq(0)").text();
        // let product_price = currentRow.find("td:eq(0)").text(); 
        // let channel_name = currentRow.find("td:eq(1)").text(); 
        // let product_url = currentRow.find("td:eq(2)").find('a').attr('href')

        let api_url = "../product/delete_product/";
        let data = { 'id': product_id };
        toggleLoading(true);
        $('#spinner-div').show();
        fetch(api_url, {
            method: 'DELETE',
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
                location.reload()
            } else if (response["success"] == false) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
                location.reload()
            }
        }).catch(function (err) {
            console.log(err);
        });
    });
});

//update button 
$(document).ready(function () {
    $("#datatable").on('click', '.btn-success', function () {
        let currentRow = $(this).closest("tr");
        let product_id = currentRow.attr('id')
        let product_url = currentRow.find("td:eq(2)").find('a').attr('href')
        // let product_name = currentRow.find("th:eq(0)").text();
        // let product_price = currentRow.find("td:eq(0)").text(); 
        // let channel_name = currentRow.find("td:eq(1)").text(); 

        let api_url = "../product/update_one_product/";
        let data = { 'input_url': product_url, 'id': product_id };
        toggleLoading(true);
        $('#spinner-div').show();
        fetch(api_url, {
            method: 'PUT',
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
                alert(response['message'])
                location.reload()
            } else if (response["success"] == false) {
                toggleLoading(false);
                $('#spinner-div').hide();
                alert(response['message']);
                location.reload()
            }
        }).catch(function (err) {
            console.log(err);
        });
    });
});


window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatable');

});
$(document).ready(function () {
    $('#datatable').dataTable({
        "bInfo": false,
        "bPaginate": false,
        "autoWidth": false,
        "ordering": true,
        "columns": [
            { "width": "70%" },
            { "width": "10%" },
            { "width": "10%" },
            { "width": "10%" },
            { "width": "10%" },
        ],
    });
});



function reset_password() {
    window.location = '../user/Reset_Password.html';

}
