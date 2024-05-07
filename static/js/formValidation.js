const form = document.querySelector('.form');
const inputs = document.querySelectorAll('.input');
const result = document.querySelector('.result');
const message = document.querySelector('.result-text')
let password;
let email;
let check = []
let dependenteValue;

document.addEventListener('DOMContentLoaded', function() {
    form.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
});

if (message){
    document.addEventListener('DOMContentLoaded', (e) => {
        setTimeout(() => {
            if (message.parentElement){
                result.style.visibility = 'hidden'
                message.parentElement.innerHTML = ''
            }
        }, 5000);
    })
}

form.addEventListener('submit', (e) => {
    e.preventDefault();
    let valid = checkInputs();
    if (valid.every(value => value === true)) {
        const btnEnviar = document.querySelector('[data-button]');
        var textoDoBotao = btnEnviar.textContent
        btnEnviar.disabled = true; 
        btnEnviar.innerText = textoDoBotao.replace(/.$/, 'ndo...');
        setTimeout(() => {
            form.submit(); 
            form.reset(); 
        }, 5000);
    }
});

function checkInputs() {
    let validate = [];
    inputs.forEach(input => {
        const inputValue = input.value.trim()
        const classInput = input.classList.value.split(' ')
        if (inputValue === '') {
            errorValidation(input, 'Preencha esse campo');
            validate.push(false)
        }
        else if(classInput.includes("passwordConfirm") && input.value.trim() !== password){
            errorValidation(passwordCheck, 'As senhas não correspondem');
            validate.push(false)
        }
        else if(classInput.includes("emailConfirm") && input.value.trim() !== email){
            errorValidation(emailCheck, 'Os e-mails não correspondem');
            validate.push(false)
        }
        /*
        else if (classInput.includes("checkbox")) {
            let isChecked = Array.from(inputs).some(input => input.type === 'checkbox' && input.checked);
            if (isChecked) {
                successValidation(input);
                validate.push(true);
                console.log(input.value)
            } else {
                errorValidation(input, 'Preencha este campo');
                validate.push(false);
            }
        }
        */
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
                validate.push(true)
            } else {
                errorValidation(check[0], 'Preencha esse campo');
                validate.push(false)
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
            validate.push(true)
        }
    });
    return validate
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