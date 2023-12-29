// seleciona o elemento da página
const pagina = document.querySelector('.home_body');

// adiciona a classe "mostrar" depois de um atraso de 1 segundo
setTimeout(() => {
  pagina.style.opacity = 1;
}, 300);

// adiciona um ouvinte de evento para a página descarregando
window.addEventListener('beforeunload', function () {
  pagina.classList.add('saindo');
});


function adicionaClasseAoRolar() {
  // seleciona a div
  const minhaDiv = document.querySelector('.doutor');

  // determina o ponto de rolagem para adicionar a classe
  const pontoDeRolagem = 700; // ajuste o valor conforme necessário

  // adiciona a classe "ativo" quando a página é rolada para o ponto
  window.addEventListener('scroll', function () {
    if (window.pageYOffset >= pontoDeRolagem) {
      minhaDiv.classList.add('doutorAtivo');
    }else{
      minhaDiv.classList.remove('doutorAtivo');
    }
  });
}

// chama a função quando a página é carregada
window.addEventListener('load', adicionaClasseAoRolar);


// abrir pop-up na página inicial

function popUpVideo() {
  let Video = document.querySelector('.popUpVideo');
  let player = document.querySelector('.player')
  Video.classList.toggle('ocultar');
  player.classList.toggle('ocultar');
}

function fecharPopUpVideo() {
  let Video = document.querySelector('.popUpVideo');
  let botaoFecharVideo = document.querySelector('.botaoFechar');
  if (botaoFecharVideo = true) {
    let fechar
    fechar = Video.classList.toggle('ocultar');
  }
}