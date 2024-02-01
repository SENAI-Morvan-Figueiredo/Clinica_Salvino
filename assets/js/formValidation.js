const formChangePassword = document.querySelector('.form');
const inputs = document.querySelectorAll('.input');
let password;
let email;
let check = []
let dependenteValue;

formChangePassword.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    inputs.forEach(input => {
        console.log(input)
        const inputValue = input.value.trim()
        const classInput = input.classList.value.split(' ')
        if (inputValue === '') {
            errorValidation(input, 'Preencha esse campo');

        }
        else if(classInput.includes("passwordConfirm") && input.value.trim() !== password){
            errorValidation(passwordCheck, 'As senhas não correspondem');
        }
        else if(classInput.includes("emailConfirm") && input.value.trim() !== email){
            errorValidation(emailCheck, 'Os e-mails não correspondem');
        }
        else if (classInput.includes("checkbox")) {
            check.push(input)
            let isChecked
            check.forEach((radio) => {
                if (radio.checked) {
                    isChecked = true
                    dependenteValue = radio.value.trim();
                }
            });
            if (isChecked === true) {
                successValidation(check[0]);
            } else {
                errorValidation(check[0], 'Preencha esse campo');
            };
        }
        else{
            if(classInput.includes("email")){
                email = inputValue
            }
            if(classInput.includes("password")){
                password = inputValue
            }
            successValidation(input);
        }
    });
}


function errorValidation(input, message) {
    const formControl = input.parentElement;
    if(formControl.classList.value.includes('option-dependence')){
        formControl.parentElement.classList.add('error');
        formControl.parentElement.classList.remove('success');
        shake(formControl.parentElement);

        const messageError = formControl.querySelector('small');
        messageError.innerHTML = message;
    } else{
        formControl.classList.add('error');
        formControl.classList.remove('success');
        shake(formControl);

        const messageError = formControl.querySelector('small');
        messageError.innerHTML = message;
    }
};

function successValidation(input) {
    const formControl = input.parentElement;
    if(formControl.classList.value.includes('option-dependence')){
        formControl.parentElement.classList.add('success');
        formControl.parentElement.classList.remove('error');
    } else{
        formControl.classList.add('success');
        formControl.classList.remove('error');
    }
};

function shake(formControl) {
    formControl.classList.add('shake');
    formControl.addEventListener('animationend', () => {
        formControl.classList.remove('shake');
    });
};