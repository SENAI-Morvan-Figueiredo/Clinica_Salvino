document.addEventListener('DOMContentLoaded', function() {

    // Pega todos os botões que têm a classe 'open-btn'
    const openButtons = document.querySelectorAll('.open-btn');

    let openMenu = null; // Variável para rastrear o menu aberto

    const closeAllMenus = () => {
        const allMenus = document.querySelectorAll('.menu');
        allMenus.forEach(menu => {
            menu.style.display = 'none';
        });
        openMenu = null; // Reseta a variável de menu aberto
    };

    openButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Previne comportamento padrão do link (caso tenha um href='#')

            // Encontra o menu relacionado a este botão
            const menu = this.nextElementSibling.nextElementSibling;

            // Verifica se este menu já está aberto
            if (menu === openMenu) {
                // Fecha o menu se já estiver aberto
                menu.style.display = 'none';
                openMenu = null; // Reseta a variável de menu aberto
            } else {
                // Fecha todos os menus antes de abrir o menu desejado
                closeAllMenus();
                // Abre o menu relacionado ao botão clicado
                menu.style.display = 'block';
                openMenu = menu; // Atualiza a variável de menu aberto
            }
        });
    });

    document.addEventListener('click', function(event) {
        const isClickInsideMenu = event.target.closest('.info');
        
        if (!isClickInsideMenu) {
            closeAllMenus();
        }
    });
});

