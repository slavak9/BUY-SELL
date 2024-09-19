const SuccessMessage = document.querySelector('.no_errors');
const objectMessage = {};

function cleanErrorMessage() {
    if (objectMessage) {
        console.log(objectMessage);
        for (let i in objectMessage) {
            objectMessage[i].textContent = ''
        }
    }
};

// cleaning field value and red border 
function cleanFormFields() {
    const formFieldsList = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'date_of_birth']
    for (id in formFieldsList) {
        const Field = document.querySelector(`#id_${formFieldsList[id]}`)
        Field.classList.remove('field_error_style')
        Field.value = ''
    };
};

// displaying error message per field
function displayFormRegErrors(errors) {
    cleanErrorMessage()
    SuccessMessage.classList.add('hidden_error');
    for (key in errors) {
        let errorMessage = document.querySelector(`#${key}_error`);
        errorMessage.classList.remove('hidden_error');
        objectMessage[key] = errorMessage
        errorMessage.innerHTML = String(errors[key]);
        if (key === 'password1' || key === 'password2') {
            for (let i = 0; i < 2; ++i) {
                let inputField = document.querySelector(`#id_password${i + 1}`)
                inputField.classList.add('field_error_style')
                inputField.addEventListener('click', () => {
                    inputField.classList.remove('field_error_style')
                });
            };
        };
        let inputField = document.querySelector(`#id_${key}`);
        inputField.classList.add('field_error_style');
        inputField.addEventListener('click', () => {
            inputField.classList.remove('field_error_style')
        });

    };
};

// displaying success message
function displayFormRegSuccess() {
    SuccessMessage.classList.remove('hidden_error');
    SuccessMessage.innerHTML = 'The data was saved successfully. To complete your registration confirm the link, that was send to your email';
    cleanFormFields();
    cleanErrorMessage();
};

// send form data via AJAX return message form the server 
document.querySelector('#registration-form-submit').addEventListener('submit', function (event) {
    event.preventDefault();
    $.ajax({
        type: 'POST',
        dataType: 'json',
        data: {
            username: $('#id_username').val(),
            password1: $('#id_password1').val(),
            password2: $('#id_password2').val(),
            email: $('#id_email').val(),
            first_name: $('#id_first_name').val(),
            last_name: $('#id_last_name').val(),
            date_of_birth: $('#id_date_of_birth').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },

        success: function (response) {
            if (response['success']) {
                displayFormRegSuccess();
            } else { displayFormRegErrors(response) }
        },
        //        failure: function (response) { alert('something went wrong'); console.log(JSON.stringify(response['f'])); console.log(response['f']); console.log('respons 2')}
    })
});
