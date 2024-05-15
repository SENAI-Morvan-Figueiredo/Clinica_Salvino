const funcionarios = document.querySelectorAll('.func')
const select = document.querySelector('#filter')

select.addEventListener('change', ()=>{
    if(select.value === 'medicos'){
        funcionarios.forEach((funcionario)=>{
            if(funcionario.classList.contains('recep')){
                funcionario.parentElement.style.display = 'none'
            } else{
                funcionario.parentElement.style.display = 'grid'
            }
        })
    } else if(select.value === 'recepcionistas'){
        funcionarios.forEach((funcionario)=>{
            if(funcionario.classList.contains('med')){
                funcionario.parentElement.style.display = 'none'
            } else{
                funcionario.parentElement.style.display = 'grid'
            }
        })
    } else{
        funcionarios.forEach((funcionario) =>{
            funcionario.parentElement.style.display = 'grid'
        })
    }
})

