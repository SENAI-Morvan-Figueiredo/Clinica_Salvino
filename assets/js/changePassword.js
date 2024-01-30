const formChangePassword = document.getElementById('form-changePassword');
const inputs = document.querySelectorAll('.input');
let password 

formChangePassword.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    inputs.forEach(input => {
        const inputValue = input.value.trim()
        const classInput = input.classList.value.split(' ')
        console.log(classInput)
        if (inputValue === '') {
            errorValidation(input, 'Preencha esse campo');

        }
        else if(classInput.includes("confirm") && input.value.trim() !== password){
            errorValidation(passwordCheck, 'As senhas não correspondem');
        }
        else {
            successValidation(input);
            password = inputValue
        }
    });
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