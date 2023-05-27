const formForgot = document.getElementById('form-forgot');
const email = document.getElementById('email');
const password = document.getElementById('code');

formForgot.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    if (emailValue === '') {
        errorValidation(email, 'Preencha esse campo');
    } else {
        successValidation(email);
    }

    if (passwordValue === '') {
        errorValidation(password, 'Preencha esse campo');
    } else {
        successValidation(password);
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