const btn_nav = document.querySelector('.btn-nav')
const nav_menu = document.querySelector('.nav_menu')

btn_nav.addEventListener('click', ()=>{
    nav_menu.style.display = 'flex'
})

nav_menu.addEventListener('click', ()=>{
    nav_menu.style.display = 'none'
})