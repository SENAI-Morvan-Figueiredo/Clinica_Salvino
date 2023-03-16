// seleciona o elemento da página
const pagina = document.querySelector('.home_body');

// adiciona a classe "mostrar" depois de um atraso de 1 segundo
setTimeout(() => {
  pagina.style.opacity = '1';
}, 300);

// adiciona um ouvinte de evento para a página descarregando
window.addEventListener('beforeunload', function() {
  pagina.classList.add('saindo');
});
