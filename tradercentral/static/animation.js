window.addEventListener('DOMContentLoaded', () => {
    const numberOfSlides = document.querySelectorAll('.slide').length;
    const pixelSpeed = numberOfSlides * 35
    const pageRoot = document.querySelector(':root');
    pageRoot.style.setProperty('--numberOfItems', numberOfSlides);
    pageRoot.style.setProperty('--pixelSpeed', `-${pixelSpeed}px`);
});