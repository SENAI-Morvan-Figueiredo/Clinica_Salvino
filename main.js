const form = document.getElementById('form-cad');
const userName = document.getElementById('Name');
const email = document.getElementById('email');
const password = document.getElementById('password');
const passwordCheck = document.getElementById('passwordCheck');
const date = document.getElementById('date');
const rg = document.getElementById('RG');
const cpf = document.getElementById('CPF');
const dependente = document.querySelectorAll('input[name="dependente"]');
let formControls = [userName, email, password, passwordCheck, date, rg, cpf];

form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    checkInputs();
});

function checkInputs() {
    const nameValue = userName.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const passwordCheckValue = passwordCheck.value.trim();
    const dateValue = date.value.trim();
    const rgValue = rg.value.trim();
    const cpfValue = cpf.value.trim();
    let dependenteValue='';

    dependente.forEach((radio) => {
        if (radio.checked) {
          dependenteValue = radio.value;
        }
      });
    console.log(dependenteValue)

    if (nameValue === '') {
        errorValidation(userName, 'Preencha esse campo');
        
    } else {
        successValidation(userName);
    };

    if (emailValue === '') {
        errorValidation(email, 'Preencha esse campo');
        
    } else {
        successValidation(email);
    };

    if (passwordValue === '') {
        errorValidation(password, 'Preencha esse campo');
    } else if (passwordValue.length < 8) {
        errorValidation(password, 'A senha deve ter 8 ou mais caracteres');  
    }else {
        successValidation(password);
    };

    if (passwordCheckValue === '') {
        errorValidation(passwordCheck, 'Preencha esse campo');
        
    } else if (passwordCheckValue !== passwordValue) {
        errorValidation(passwordCheck, 'As senhas são diferentes');
    } else {
        successValidation(passwordCheck);
    };

    if (dateValue === '') {
        errorValidation(date, 'Preencha esse campo');
        
    } else {
        successValidation(date);
    };

    if (rgValue === '') {
        errorValidation(rg, 'Preencha esse campo');
        
    } else {
        successValidation(rg);
    };

    if (cpfValue === '') {
        errorValidation(cpf, 'Preencha esse campo');
        
    } else {
        successValidation(cpf);
    };
};


function errorValidation(input, message) {
    const formControl = input.parentElement;
    formControl.classList.add('error');
    formControl.classList.remove('success');

    shake(formControl);

    const messageError = formControl.querySelector('small');
    messageError.innerHTML = message;
};

function successValidation(input) {
    const formControl = input.parentElement;
    formControl.classList.add('success');
    formControl.classList.remove('error');
};

function shake (formControl){
    formControl.classList.add('shake');
    formControl.addEventListener('animationend', ()=>{
        formControl.classList.remove('shake');
    });
};