const formChangeEmail = document.getElementById('form-changeEmail');
const email = document.getElementById('email');
const newEmail = document.getElementById('newEmail');
const emailCheck = document.getElementById('emailCheck');

formChangeEmail.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    const emailValue = email.value.trim();
    const newEmailValue = newEmail.value.trim();
    const emailCheckValue = emailCheck.value.trim();

    if (emailValue === '') {
        errorValidation(email, 'Preencha esse campo');
    } else {
        successValidation(email);
    }

    if (newEmailValue === '') {
        errorValidation(newEmail, 'Preencha esse campo');
    } else {
        successValidation(newEmail);
    }

    if (emailCheckValue === '') {
        errorValidation(emailCheck, 'Preencha esse campo');
    } else if (emailCheckValue !== newEmailValue) {
        errorValidation(emailCheck, 'Os e-mails não correspondem');
    } else {
        successValidation(emailCheck);
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