const nav = document.querySelector('.nav-home');
const logo = document.querySelector('.logo-home');
const container = document.querySelector('.nav');
const login = document.querySelector('.login');
const menuAb = document.querySelector('.menu-ab')

function scrollPosition(){
    if(window.scrollY>40){
        nav.classList.remove('animate');
        logo.classList.add('animatelogo');
        container.classList.add('align-items-center');
        if(login){
            login.style.marginTop= 0;
        } else if(menuAb){
            menuAb.style.top= '90px'
            menuAb.style.right= '160px'
        }
        
    } else{
        nav.classList.add('animate');
        logo.classList.remove('animatelogo');
        container.classList.remove('align-items-center');
        if(login){
            login.style.marginTop= '10px'
        } else if(menuAb){
            menuAb.style.top= '80px'
            menuAb.style.right= '150px'
        }
        
    }
}
scrollPosition();


window.addEventListener('scroll', scrollPosition);

