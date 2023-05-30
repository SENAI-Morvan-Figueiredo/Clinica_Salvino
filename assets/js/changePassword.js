const formChangeEmail = document.getElementById('form-changePassword');
const password = document.getElementById('password');
const newPassword = document.getElementById('newPassword');
const passwordCheck = document.getElementById('passwordCheck');

formChangeEmail.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    const passwordValue = password.value.trim();
    const newPasswordValue = newPassword.value.trim();
    const passwordCheckValue = passwordCheck.value.trim();

    if (passwordValue === '') {
        errorValidation(password, 'Preencha esse campo');
    } else {
        successValidation(password);
    }

    if (newPasswordValue === '') {
        errorValidation(newPassword, 'Preencha esse campo');
    } else if (newPasswordValue === passwordValue){
        errorValidation(newPassword, 'Use uma senha diferente da anterior');
    }
    else{
        successValidation(newPassword);
    }

    if (passwordCheckValue === '') {
        errorValidation(passwordCheck, 'Preencha esse campo');
    } else if (passwordCheckValue !== newPasswordValue) {
        errorValidation(passwordCheck, 'As senhas não correspondem');
    } else {
        successValidation(passwordCheck);
    }
}


function errorValidation(input, message) {
    const formControl = input.parentElement;
    formControl.classList.add('error');
    formControl.classList.remove('success');
    
    const messageError = formControl.querySelector('small');
    messageError.innerHTML = message;

    shake(formControl);
};

function successValidation(input) {
    const formControl = input.parentElement;
    formControl.classList.add('success');
    formControl.classList.remove('error');
};

function shake(formControl) {
    formControl.classList.add('shake');
    formControl.addEventListener('animationend', () => {
        formControl.classList.remove('shake');
    });
};