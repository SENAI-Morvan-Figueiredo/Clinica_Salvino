// seleciona o elemento da página
const pagina = document.querySelector('.home_body');

// adiciona a classe "mostrar" depois de um atraso de 1 segundo
setTimeout(() => {
  pagina.style.opacity = 1;
}, 300);

// adiciona um ouvinte de evento para a página descarregando
window.addEventListener('load', adicionaClasseAoRolar);

window.addEventListener('scroll', adicionaClasseAoRolar);

function adicionaClasseAoRolar() {
  // seleciona a div
  const minhaDiv = document.querySelector('.doutor');
  // define a posição do scroll
  const posicaoScroll = window.pageYOffset;

  // adiciona a classe "ativo" quando a página é rolada para o ponto e desativa
  if (posicaoScroll >= 821 && posicaoScroll < 1859) {
    minhaDiv.classList.add('doutorAtivo');
  } else {
    minhaDiv.classList.remove('doutorAtivo');
  }
}

// abrir pop-up na página inicial
function popUpVideo() {
  let Video = document.querySelector('.popUpVideo');
  Video.classList.toggle('ocultar');
}

function fecharPopUpVideo() {
  let Video = document.querySelector('.popUpVideo');
  let botaoFecharVideo = document.querySelector('.botaoFechar');
  if (botaoFecharVideo = true) {
    let fechar
    fechar = Video.classList.toggle('ocultar');
  }
}