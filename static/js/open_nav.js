const btn_nav = document.querySelector('.btn-nav')
const background = document.querySelector('.nav_menu')
const nav_menu = document.querySelector('.dash_menu_user')

btn_nav.addEventListener('click', ()=>{
    background.style.display = 'flex'
    nav_menu.style.display = 'flex'
})

background.addEventListener('click', ()=>{
    console.log(nav_menu)
    background.style.display = 'none'
    nav_menu.style.display = 'none'
})