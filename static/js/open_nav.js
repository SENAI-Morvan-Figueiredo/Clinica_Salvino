const btn_nav = document.querySelector('.btn-nav')
const background = document.querySelector('.nav_menu')
const nav_menu = document.querySelector('.dash_menu_user')
const close_button = document.querySelector('.close_button')

btn_nav.addEventListener('click', ()=>{
    background.classList.add('ativo');
    nav_menu.classList.add('ativo');
    close_button.classList.add('ativo');
});

close_button.addEventListener('click', ()=>{
    background.classList.remove('ativo');
    nav_menu.classList.remove('ativo');
    close_button.classList.remove('ativo');
});

function resetStylesOnHeightChange() {
    if (window.innerWidth > 880) {
        background.classList.remove('ativo');
        nav_menu.classList.add('ativo');
        close_button.classList.remove('ativo');
    } else {
        background.classList.remove('ativo');
        nav_menu.classList.remove('ativo');
        close_button.classList.remove('ativo');
    }
}

window.addEventListener('resize', resetStylesOnHeightChange);

// Chama a função para garantir o estado inicial correto
resetStylesOnHeightChange();

nav_menu.addEventListener('touchmove', function (event) {
    event.stopPropagation();
}, false);
