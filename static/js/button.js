const forms = document.querySelectorAll('form')

function voltar(){
    forms.forEach((form) =>{
        form.addEventListener('submit', (event)=>{
            event.preventDefault()
        })
    })
    history.back();
}

function redirect(){
    window.location.href = "/login"
}