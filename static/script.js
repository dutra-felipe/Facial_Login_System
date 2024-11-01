const menu = document.querySelector('.btn-menu');
const menuMobile = document.querySelector('.menu-mobile');
const linksMobile = document.querySelectorAll('.link-mobile');

menu.addEventListener('click', () => {
    menu.classList.toggle('ativo');
    menuMobile.classList.toggle('ativo');
   
    if (menuMobile.classList.contains('ativo')) {
        document.body.style.overflow = 'hidden';
        
        linksMobile.forEach(link => {
            link.addEventListener('click', () => {
                document.body.style.overflow = '';
                menu.classList.remove('ativo');
                menuMobile.classList.remove('ativo');
            });
        });
    } else {
        document.body.style.overflow = '';
    }
});