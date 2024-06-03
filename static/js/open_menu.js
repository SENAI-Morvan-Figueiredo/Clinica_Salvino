document.addEventListener('DOMContentLoaded', function() {

    // Pega todos os botões que têm a classe 'open-btn'
    const openButtons = document.querySelectorAll('.open-btn');

    const closeAllMenus = () => {
        const allMenus = document.querySelectorAll('.menu');
        allMenus.forEach(menu => {
            menu.style.display = 'none';
        });
    };

    openButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Previne comportamento padrão do link (caso tenha um href='#')

            // Encontra o menu relacionado a este botão
            const menu = this.nextElementSibling.nextElementSibling;

            // Alterna a visibilidade do menu
            if (menu.style.display === 'none' || menu.style.display === '') {
                menu.style.display = 'block';
            } else {
                menu.style.display = 'none';
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

