// Scroll Position
let scrollY = 0;

// Varaible use for the scroll event.
let ticking = false;

/**
 * Regulates the scroll event.
 * Only perform `updateNavbar()` once at a time (When ticking is true).
 * The return value is 'baz' in all cases.
 * Because Repaint Is Expensive.
 */
document.addEventListener('scroll', (e)=>{
    scrollY = window.pageYOffset
    if (!ticking) {
        window.requestAnimationFrame(() => {
            updateNavbar(scrollY);
        ticking = false;
        });
    
        ticking = true;
    }
});

/**
 * Updates the classlist of the Navigation Bar
 * to apply css effects.
 */
function updateNavbar() {
    if(scrollY > 20) {
        document.getElementById('nav-bar').classList.add('navBar-scrolled');
    }else {
        document.getElementById('nav-bar').classList.remove('navBar-scrolled');
    }
}