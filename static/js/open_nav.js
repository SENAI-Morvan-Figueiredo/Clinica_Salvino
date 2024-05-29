const btn_nav = document.querySelector('.btn-nav')
const background = document.querySelector('.nav_menu')
const nav_menu = document.querySelector('.dash_menu_user')

btn_nav.addEventListener('click', ()=>{
    background.style.display = 'flex'
    nav_menu.style.display = 'flex'
})

background.addEventListener('click', ()=>{
    background.style.display = 'none'
    nav_menu.style.display = 'none'
})

function resetStylesOnHeightChange() {
    if (window.innerWidth > 880) {
        background.style.display = 'none';
        nav_menu.style.display = 'block';
    } else {
        background.style.display = 'none';
        nav_menu.style.display = 'none';
    }
}

window.addEventListener('resize', resetStylesOnHeightChange);

// Chama a função para garantir o estado inicial correto
resetStylesOnHeightChange();
