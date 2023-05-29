const form = document.getElementById('form-cad');
const userName = document.getElementById('Name');
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
let formControls = [userName, date, rg, cpf, responsavel, phone];

form.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    const nameValue = userName.value.trim();
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

    if (nameValue === '') {
        errorValidation(userName, 'Preencha esse campo');

    } else {
        successValidation(userName);
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