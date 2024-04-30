const form = document.querySelector('.form')
const select = document.querySelector('#register')
const message = document.querySelector('.result-text')
const result = document.querySelector('.result');

select.addEventListener('change', ()=>{
    form.submit()
})

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
