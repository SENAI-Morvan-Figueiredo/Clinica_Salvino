const forms = document.querySelectorAll('.form')
const select = document.querySelector('#register')

document.addEventListener('DOMContentLoaded', ()=>{
    forms.forEach((form)=>{
        form.style.display = 'none'
    })
    
    select.style.alignSelf = 'flex-start'
})

select.addEventListener('change', ()=>{
    if(select.value === 'medico'){
        forms.forEach((form)=>{
            if(form.classList.contains('recep')){
                form.style.display = 'none'
            } else{
                form.style.display = 'flex'
                select.style.alignSelf = 'center'
            }
        })
    } else if(select.value === 'recepcionista'){
        forms.forEach((form)=>{
            if(form.classList.contains('med')){
                form.style.display = 'none'
            } else{
                form.style.display = 'flex'
                select.style.alignSelf = 'center'
            }
        })
    } else{
        forms.forEach((form) =>{
            form.style.display = 'none'
            select.style.alignSelf = 'flex-start'
        })
    }
})

