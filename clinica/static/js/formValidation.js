const form = document.querySelector('.form');
const inputs = document.querySelectorAll('.input');
const result = document.querySelector('.result');
const message = document.querySelector('.result-text')
let password;
let email;
let check = []
let dependenteValue;

document.addEventListener('DOMContentLoaded', (e) => {
    setTimeout(() => {
        message.innerHTML = ''
    }, 5000);
})

form.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevenir o envio padrão do formulário
    let check = checkInputs();
    if (check.every(value => value === true)) {
        console.log("Todos os campos estão válidos. Redirecionando...");
        const btnEnviar = document.querySelector('[data-button]');
        btnEnviar.disabled = true; // Desativar o botão
        btnEnviar.innerText = "Enviando..."; // Alterar o texto do botão
        setTimeout(() => {
            form.submit(); // Enviar o formulário após 5 segundos
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
        else if (classInput.includes("checkbox")) {
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