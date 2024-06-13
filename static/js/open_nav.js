const btn_nav = document.querySelector('.btn-nav')
const background = document.querySelector('.nav_menu')
const nav_menu = document.querySelector('.dash_menu_user')
const close_button = document.querySelector('.close_button')

btn_nav.addEventListener('click', ()=>{
    background.style.display = 'flex'
    nav_menu.style.display = 'flex'
    close_button.style.display = 'block'
})

close_button.addEventListener('click', ()=>{
    background.style.display = 'none'
    nav_menu.style.display = 'none'
    close_button.style.display = 'none'
})

function resetStylesOnHeightChange() {
    if (window.innerWidth > 880) {
        background.style.display = 'none';
        nav_menu.style.display = 'block';
        close_button.style.display = 'none'
    } else {
        background.style.display = 'none';
        nav_menu.style.display = 'none';
        close_button.style.display = 'none'
    }
}

window.addEventListener('resize', resetStylesOnHeightChange);

// Chama a função para garantir o estado inicial correto
resetStylesOnHeightChange();
