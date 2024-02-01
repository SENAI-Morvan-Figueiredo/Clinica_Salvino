class FormSubmit {
    constructor(settings) {
        this.settings = settings;
        this.form = document.querySelector(settings.form);
        this.formButton = document.querySelector(settings.button);
        if (this.form) {
            this.url = this.form.getAttribute("action");
        };
        this.sendForm = this.sendForm.bind(this);
        this.name = document.getElementById('nome');
        this.email = document.getElementById('email');
        this.subject = document.getElementById('subject');
        this.message = document.getElementById('message');
        this.result = document.querySelector('.result')
        this.resultMesssage = document.querySelector('.result-text')
        this.shake = shake;
        this.formControls = [this.name, this.email, this.subject, this.message];

        this.setupEventListeners();
    };

    resetForm() {
        this.form.reset();
        this.formControls.forEach((input) => {
            input.parentElement.classList.remove("success");
        });
    }

    resetForm() {
        this.form.reset();
        this.formControls.forEach((input) => {
            input.parentElement.classList.remove("success");
        });
    }

    restart() {
        this.formButton.removeEventListener("click", this.sendForm);
        this.formButton.addEventListener('click', (event) => {
            event.preventDefault();
            formSubmit.sendForm(event);
        });
        this.formButton.disabled = false;
        this.formButton.innerText = "Enviar";
        setTimeout(() => {
            if (this.result.classList.contains('success')) {
                this.result.classList.remove('success');
            }
            if (this.result.classList.contains('error')) {
                this.result.classList.remove('error');
            }
            this.resultMesssage.innerHTML = '';
        }, 3500)
    }

    displaySuccess() {
        this.result.classList.add('success')
        this.resultMesssage.innerHTML = this.settings.success;
        this.resetForm()
        this.restart()
    }

    displayError() {
        if (this.result.classList.contains('success')) {
            this.result.classList.remove('success')
        };
        this.result.classList.add('error')
        this.resultMesssage.innerHTML = this.settings.error;
        this.resetForm()
        this.restart()
    }

    getFormObject() {
        const formObject = {};
        const fields = this.form.querySelectorAll("[name]")
        fields.forEach((field) => {
            formObject[field.getAttribute('name')] = field.value;
        });

        return formObject;
    }

    onSubmission(event) {
        event.preventDefault();
        event.target.disabled = true;
        event.target.innerText = "Enviando...";
    }

    setupEventListeners() {
        this.formControls.forEach((input) => {
            input.addEventListener("input", () => {
                input.parentElement.classList.remove("error");
            });
        });
    }

    errorAnimation(parentElement, type) {
        if (type !== '') {
            parentElement.classList.add('error');
            parentElement.classList.remove('success');
            this.shake(parentElement);
        }
    }

    errorMessage(parentElement, type) {
        const messageError = parentElement.querySelector('small');
        if (type === 'empty') {
            messageError.innerHTML = this.settings.empty;
        } else if (type === 'invalid email') {
            messageError.innerHTML = this.settings.invalidEmail;
        }
    }

    validateEmail(element) {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailRegex.test(element.value);
    }
    

    errorValidation() {
        this.formControls.forEach((input) => {
            const parentElement = input.parentElement;
            const value = input.value.trim();
            let type = '';
            
            if (value === '') {
                type = 'empty';
            } else if (input === this.email && !this.validateEmail(input)) {
                type = 'invalid email';
            }
            
            this.errorAnimation(parentElement, type);
            this.errorMessage(parentElement, type);
            return;
        });
    }
    


    async sendForm(event) {
        try {
            event.preventDefault();
            
            // Verificar se os campos estão preenchidos corretamente
            const formIsValid = this.form.checkValidity();
            if (!formIsValid) {
                this.errorValidation();
                return;
            }
            
            // Verificar se o e-mail é válido
            if (!this.validateEmail(this.email)) {
                this.errorValidation();
                return;
            }
    
            this.onSubmission(event);
            await fetch(this.url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json",
                },
                body: JSON.stringify(this.getFormObject()),
            });
            this.displaySuccess();
        } catch (error) {
            this.displayError();
            throw new Error(error);
        }
    }
    

    init() {
        if (this.form) this.formButton.addEventListener("click", this.sendForm);
        return this;
    }
}

const formSubmit = new FormSubmit({
    form: "[data-form]",
    button: "[data-button]",
    success: "<p class='success'>Formulário enviado!</p>",
    error: "<p class='error'>Erro!</p>",
    invalidEmail: "<p class='error'>Digite um e-mail válido</p>",
    empty: "<p class='error'>Preencha esse campo</p>"
});
function shake(element) {
    element.classList.add('shake');
    element.addEventListener('animationend', () => {
        element.classList.remove('shake');
    }, { once: true });
}

formSubmit.init();