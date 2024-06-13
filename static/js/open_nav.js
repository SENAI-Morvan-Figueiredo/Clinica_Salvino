document.addEventListener('DOMContentLoaded', function () {
    const btn_nav = document.querySelector('.btn-nav');
    const background = document.querySelector('.nav_menu');
    const nav_menu = document.querySelector('.dash_menu_user');
    const close_button = document.querySelector('.close_button');

    btn_nav.addEventListener('click', () => {
        console.log('Menu aberto');
        background.classList.add('ativo');
        nav_menu.classList.add('ativo');
        close_button.classList.add('ativo');
    });

    close_button.addEventListener('click', () => {
        console.log('Menu fechado');
        background.classList.remove('ativo');
        nav_menu.classList.remove('ativo');
        close_button.classList.remove('ativo');
    });

    function resetStylesOnResize() {
        if (window.innerWidth > 880) {
            console.log('Largura maior que 880px, ajustando estilos');
            background.classList.remove('ativo');
            nav_menu.classList.add('ativo');
            close_button.classList.remove('ativo');
        } else {
            console.log('Largura menor ou igual a 880px, ajustando estilos');
            background.classList.remove('ativo');
            nav_menu.classList.remove('ativo');
            close_button.classList.remove('ativo');
        }
    }

    window.addEventListener('resize', resetStylesOnResize);

    // Chama a função para garantir o estado inicial correto
    resetStylesOnResize();

    // Previne o fechamento ao scroll dentro do menu
    nav_menu.addEventListener('touchmove', function (event) {
        console.log('Touchmove no menu');
        event.stopPropagation();
    }, false);
});