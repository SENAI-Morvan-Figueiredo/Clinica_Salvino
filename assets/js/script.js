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


function adicionaClasseAoRolar() {
    // seleciona a div
    const minhaDiv = document.querySelector('.doutor');
  
    // determina o ponto de rolagem para adicionar a classe
    const pontoDeRolagem = 700; // ajuste o valor conforme necessário
  
    // adiciona a classe "ativo" quando a página é rolada para o ponto
    window.addEventListener('scroll', function() {
      if (window.pageYOffset >= pontoDeRolagem) {
        minhaDiv.classList.add('doutorAtivo');
      } 
    });
  }
  
  // chama a função quando a página é carregada
  window.addEventListener('load', adicionaClasseAoRolar);
  