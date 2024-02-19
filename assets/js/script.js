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
  const doc = document.documentElement
  console.log(minhaDiv.getBoundingClientRect())
  // adiciona a classe "ativo" quando a página é rolada para o ponto e desativa

  if (window.screen.height >= 1225){
    if (minhaDiv.getBoundingClientRect()['y'] < 1322 && minhaDiv.getBoundingClientRect()['y'] > -465) {
      minhaDiv.classList.add('doutorAtivo');
    } else {
      minhaDiv.classList.remove('doutorAtivo');
    }
  } else if(minhaDiv.getBoundingClientRect()['weight'] >= 663) {
    if (minhaDiv.getBoundingClientRect()['y'] < 918 && minhaDiv.getBoundingClientRect()['y'] > -620) {
      minhaDiv.classList.add('doutorAtivo');
    } else {
      minhaDiv.classList.remove('doutorAtivo');
    }
  } else{
    if (minhaDiv.getBoundingClientRect()['y'] < 918 && minhaDiv.getBoundingClientRect()['y'] > -420) {
      minhaDiv.classList.add('doutorAtivo');
    } else {
      minhaDiv.classList.remove('doutorAtivo');
    }
  }
}

// abrir pop-up na página inicial
class PopUpAbrir {
  /**
  * @param  element
  */
  constructor(element) {
    this.elemento = element;
    this.elemento.classList.toggle('ocultar');
  }
}

class FecharPopUp {
  /**
   * @param botao
   */
  constructor(botao) {
    let elemento1 = botao.parentElement
    let elemento2 = elemento1.parentElement
    let popUp = elemento2.parentElement
    if (botao = true) {
      let fechar;
      fechar = popUp.classList.toggle('ocultar');
    }
  }

}

function abrirPopUp() {
  let popUp;
  elemento = `.popUp${event.target.classList['0']}`
  console.log(elemento)
  popUp = new PopUpAbrir(document.querySelector(elemento));
}

function fecharPopUp(event) {
  let fechar
  fechar = new FecharPopUp(event.target)
}