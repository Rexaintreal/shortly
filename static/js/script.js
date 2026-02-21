const cat = document.getElementById('dvd-car')
let x = 100, y= 100;
let dx = 2, dy=2;
let enabled = true;

function moveCat(){
    if (!enabled) return;

    x+= dx;
    y+= dy;

    if (x + cat.offsetWidth >= window.innerWidth || x <= 0) dx = -dx;
    if (y + cat.offsetHeight >= window.innerHeight || y <= 0) dy = -dy;

    cat.style.left =x +'px';
    cat.style.top = y + 'px';

    requestAnimationFrame(moveCat);
}

function toggleCat() {
    enabled = !enabled;
    const knob = document.getElementById('toggle-knob');
    const toggle = document.getElementById('toggle');
    cat.style.display = enabled ? 'block' : 'none';
    toggle.style.background = enabled ? '#F5F5F5' : '#24262B';
    knob.style.left = enabled ? '22px' : '2px';
    if (enabled) moveCat();
}

function changeSpeed(val) {
    document.getElementById('speed-val').textContent = val;
    const dir = (n) => n > 0 ? 1 : -1;
    dx = dir(dx) * parseInt(val);
    dy = dir(dy) * parseInt(val);
}

function changeSize(val) {
    cat.style.width = val + 'px';
    document.getElementById('size-val').textContent = val + 'px';
}


function toggleMenu() {
    const menu = document.getElementById('settings');
    menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
}

lucide.createIcons();
moveCat();
