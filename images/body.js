$(function(){
    
    var $g_banner_owl
    $g_banner_owl = $('#momoStyle_g-banner-owl.momoStyle_owl-carousel').owlCarousel({
        loop: true,
        nav: false,
        margin: 0,
        dots: false,
        items: 1,
        autoplay: true,
        autoplayTimeout: 4500
    })
    $('#momoStyle_g-banner-btn-prev').click(function(){
        $g_banner_owl.trigger('prev.owl.carousel')
    })
    $('#momoStyle_g-banner-btn-next').click(function(){
        $g_banner_owl.trigger('next.owl.carousel')
    })

    var myLazyLoad = new LazyLoad({
        elements_selector: ".momoStyle_lazyload"
    });

})
