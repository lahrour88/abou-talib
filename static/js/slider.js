document.addEventListener('DOMContentLoaded', function() {
    const sliders = document.querySelectorAll('.post-slider');
    
    sliders.forEach(function(slider) {
        new Swiper(slider, {
            slidesPerView: 1,
            spaceBetween: 1,
            loop: true,
            autoHeight: true,
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            effect: 'fade',
            fadeEffect: {
                crossFade: true
            }
        });
    });
});
