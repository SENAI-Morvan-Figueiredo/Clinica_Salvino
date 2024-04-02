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

  if (window.screen.height > 1000) {
    if (minhaDiv.getBoundingClientRect()['y'] < 1200 && minhaDiv.getBoundingClientRect()['y'] > -465) {
      minhaDiv.classList.add('doutorAtivo');
    } else {
      minhaDiv.classList.remove('doutorAtivo');
    }
  } else {
    if (minhaDiv.getBoundingClientRect()['height'] <= 552) {
      if (minhaDiv.getBoundingClientRect()['y'] < 658 && minhaDiv.getBoundingClientRect()['y'] > -522) {
        minhaDiv.classList.add('doutorAtivo');
      } else {
        minhaDiv.classList.remove('doutorAtivo');
      }
    } else if(minhaDiv.getBoundingClientRect()['height'] <= 663){
      if (minhaDiv.getBoundingClientRect()['y'] < 574 && minhaDiv.getBoundingClientRect()['y'] > -755) {
        minhaDiv.classList.add('doutorAtivo');
      } else {
        minhaDiv.classList.remove('doutorAtivo');
      }
    }else if(minhaDiv.getBoundingClientRect()['height'] <= 870){
      if (minhaDiv.getBoundingClientRect()['y'] < 574 && minhaDiv.getBoundingClientRect()['y'] > -825) {
        minhaDiv.classList.add('doutorAtivo');
      } else {
        minhaDiv.classList.remove('doutorAtivo');
      }
    } else{
      if (minhaDiv.getBoundingClientRect()['y'] < 574 && minhaDiv.getBoundingClientRect()['y'] > -910) {
        minhaDiv.classList.add('doutorAtivo');
      } else {
        minhaDiv.classList.remove('doutorAtivo');
      }
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