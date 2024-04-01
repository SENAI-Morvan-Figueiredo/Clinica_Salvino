const nav = document.querySelector('.nav-home');
const logo = document.querySelector('.logo-home');
const container = document.querySelector('.nav');
const login = document.querySelector('.login');

function scrollPosition(){
    if(window.scrollY>40){
        nav.classList.remove('animate');
        logo.classList.add('animatelogo');
        container.classList.add('align-items-center');
        login.style.marginTop= 0;
    } else{
        nav.classList.add('animate');
        logo.classList.remove('animatelogo');
        container.classList.remove('align-items-center');
        login.style.marginTop= '10px'
    }
}
scrollPosition();


window.addEventListener('scroll', scrollPosition);

