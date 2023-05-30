const form = document.getElementById('form-cad-card');
const userName = document.getElementById('Name');
const date = document.getElementById('vencimento');
const card = document.getElementById('number-card');
const cvc = document.getElementById('CVC');
let formControls = [userName, date, card, cvc];

form.addEventListener('submit', (e) => {
    e.preventDefault();

    checkInputs();
});

function checkInputs() {
    const nameValue = userName.value.trim();
    const dateValue = date.value.trim();
    const cardValue = card.value.trim();
    const cvcValue = cvc.value.trim();

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

    if (cardValue === '') {
        errorValidation(card, 'Preencha esse campo');

    } else {
        successValidation(card);
    };

    if (cvcValue === '') {
        errorValidation(cvc, 'Preencha esse campo');

    } else {
        successValidation(cvc);
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