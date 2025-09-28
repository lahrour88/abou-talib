//jquery-click-scroll
//by syamsul'isul' Arifin

document.addEventListener('DOMContentLoaded', function() {
    // التحقق من وجود jQuery
    if (typeof jQuery === 'undefined') {
        console.error('هذا السكربت يتطلب jQuery');
        return;
    }

    var sectionArray = [1, 2, 3, 4, 5];

    $.each(sectionArray, function(index, value){
        $(document).scroll(function(){
            var section = $('#section_' + value);
            
            // التحقق من وجود القسم قبل محاولة الوصول إلى offset
            if (section.length) {
                var offsetSection = section.offset().top - 75;
                var docScroll = $(document).scrollTop();
                var docScroll1 = docScroll + 1;
                
                if (docScroll1 >= offsetSection) {
                    $('.navbar-nav .nav-item .nav-link').removeClass('active');
                    $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');  
                    $('.navbar-nav .nav-item .nav-link').eq(index).addClass('active');
                    $('.navbar-nav .nav-item .nav-link').eq(index).removeClass('inactive');
                }
            }
        });
        
        $('.click-scroll').eq(index).click(function(e){
            var section = $('#section_' + value);
            
            // التحقق من وجود القسم قبل محاولة الوصول إلى offset
            if (section.length) {
                var offsetClick = section.offset().top - 75;
                e.preventDefault();
                $('html, body').animate({
                    'scrollTop': offsetClick
                }, 300);
            }
        });
    });

    // إضافة الحالة الأولية للقائمة
    if ($('.navbar-nav .nav-item .nav-link:link').length) {
        $('.navbar-nav .nav-item .nav-link:link').addClass('inactive');    
        $('.navbar-nav .nav-item .nav-link').eq(0).addClass('active');
        $('.navbar-nav .nav-item .nav-link:link').eq(0).removeClass('inactive');
    }
});