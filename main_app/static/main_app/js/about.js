document.querySelector('#form-submit').addEventListener('submit', function (event) {
    event.preventDefault();
    let forrm = new FormData(event.target);
    var forrm1 = $('#form-submit')
    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: {
            product_id: 'text',
            quantity: '5',
            header: { 'X-CSRFtoken': '{% csrf_token %}' },
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            alert('was send');
            console.log(response['res_from_serv'])

        },
        failure: function (response) { alert('something went wrong'); console.log(response['res_from_serv']) }
    })
})