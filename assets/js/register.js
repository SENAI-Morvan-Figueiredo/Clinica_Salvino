const form = document.getElementById('form-cad');
const userName = document.getElementById('Name');
const email = document.getElementById('email');
const password = document.getElementById('password');
const passwordCheck = document.getElementById('passwordCheck');
const date = document.getElementById('date');
const rg = document.getElementById('RG');
const cpf = document.getElementById('CPF');
const responsavel = document.getElementById('responsavel');
const RGresponsavel = document.getElementById('RGResponsavel');
const CPFresponsavel = document.getElementById('CPFResponsavel');
const phone = document.getElementById('phone');
const cep = document.getElementById('CEP');
const adress = document.getElementById('Endereco');
const number = document.getElementById('Numero');
const complement = document.getElementById('Complemento');
const emailCheck = document.getElementById('emailCheck');
const dependente = document.querySelectorAll('input[name="dependente"]');
let formControls = [userName, email, password, passwordCheck, date, rg, cpf, responsavel, RGresponsavel, CPFresponsavel, phone, cep, adress, number, complement, emailCheck, dependente];
let confirmar;

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
    const responsavelValue = responsavel.value.trim();
    const RGresponsavelValue = RGresponsavel.value.trim();
    const CPFresponsavelValue = CPFresponsavel.value.trim();
    const phoneValue = phone.value.trim();
    const cepValue = cep.value.trim();
    const adressValue = adress.value.trim();
    const numberValue = number.value.trim();
    const complementValue = complement.value.trim();
    const emailCheckValue = emailCheck.value.trim();
    let dependenteValue = '';
    const dependenteArray = Array.from(dependente);

    dependenteArray.forEach((radio) => {
        if (radio.checked) {
            dependenteValue = radio.value.trim();
        }
    });
    console.log(dependenteValue);

    if (dependenteValue === '') {
        errorValidation(dependente[0], 'Preencha esse campo');

    } else {
        successValidation(dependente[0]);
    };

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
    } else {
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

    if (responsavelValue === '') {
        errorValidation(responsavel, 'Preencha esse campo');

    } else {
        successValidation(responsavel);
    };

    if (RGresponsavelValue === '') {
        errorValidation(RGresponsavel, 'Preencha esse campo');

    } else {
        successValidation(RGresponsavel);
    };

    if (CPFresponsavelValue === '') {
        errorValidation(CPFresponsavel, 'Preencha esse campo');

    } else {
        successValidation(CPFresponsavel);
    };

    if (phoneValue === '') {
        errorValidation(phone, 'Preencha esse campo');

    } else {
        successValidation(phone);
    };

    if (cepValue === '') {
        errorValidation(cep, 'Preencha esse campo');

    } else {
        successValidation(cep);
    };

    if (adressValue === '') {
        errorValidation(adress, 'Preencha esse campo');

    } else {
        successValidation(adress);
    };

    if (numberValue === '') {
        errorValidation(number, 'Preencha esse campo');

    } else {
        successValidation(number);
    };

    if (complementValue === '') {
        errorValidation(complement, 'Preencha esse campo');

    } else {
        successValidation(complement);
    };

    if (emailCheckValue === '') {
        errorValidation(emailCheck, 'Preencha esse campo');
    } else if (emailCheckValue !== emailValue) {
        errorValidation(emailCheck, 'Os e-mails são diferentes');
    } else {
        successValidation(emailCheck);
    };
};


function errorValidation(input, message) {
    const formControl = input.parentElement;
    formControl.classList.add('error');
    formControl.classList.remove('success');

    shake(formControl);

    const messageError = formControl.querySelector('small');
    messageError.innerHTML = message;

    if (input instanceof NodeList) {
        // Para cada elemento da NodeList, adiciona a classe 'error' ao elemento pai
        // e exibe a mensagem de erro correspondente
        input.forEach((item) => {
            const formControl = item.parentElement;
            formControl.classList.add('error');
            formControl.classList.remove('success');

            shake(formControl);

            const messageError = formControl.querySelector('small');
            messageError.innerHTML = message;
        });
    } else {
        const formControl = input.parentElement;
        formControl.classList.add('error');
        formControl.classList.remove('success');

        shake(formControl);

        const messageError = formControl.querySelector('small');
        messageError.innerHTML = message;
    }
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

function voltar(){
    history.back();
}

function redirect(){
    window.location.href = "login.html"
}
