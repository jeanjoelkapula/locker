var el = null;
        var btn = null;
        var menu = null;
        var visible = false;

        window.addEventListener('DOMContentLoaded', (event) => {
            console.log('this');
            $('.more-menu-btn').on('click', function(){
                console.log(this.href);
            });
        });

function showMenu(e) {
    e.preventDefault();
        
        btn = this;
        el = btn.parentNode;
        menu = el.querySelector('.more-menu');
    if (!visible) {
        visible = true;
        el.classList.add('show-more-menu');
        menu.setAttribute('aria-hidden', false);
        document.addEventListener('mousedown', hideMenu, false);
    }
}

function hideMenu(e) {
    more = document.querySelector('.more-menu-btn');

    if (btn.contains(e.target) || e.target.className == 'more-menu-btn') {
        return;
    }

    if (visible) {
        visible = false;
        el.classList.remove('show-more-menu');
        menu.setAttribute('aria-hidden', true);
        document.removeEventListener('mousedown', hideMenu);
    }
}

$('.more-btn').on('click', showMenu);