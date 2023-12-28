const debounce = (func, wait, immediate, timeout) => 
(...args) => {
        const later =  () => {
            if (!immediate) func(args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(args);
    };

const nav = document.querySelector('.nav-home');
const logo = document.querySelector('.logo-home');
const container = document.querySelector('.nav');
const login = document.querySelector('.login');

function scrollPosition(){
    if(window.scrollY>40){
        nav.classList.remove('animate');
        console.log(logo)
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


window.addEventListener('scroll', debounce(() => {
    scrollPosition();
}, 200));

