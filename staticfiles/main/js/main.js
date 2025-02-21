(function ($) {
    "use strict";

    $(document).ready(function () {
        // Spinner
        var spinner = function () {
            setTimeout(function () {
                if ($('#spinner').length > 0) {
                    $('#spinner').removeClass('show');
                }
            }, 1);
        };
        spinner();

        // Initiate WOW.js
        new WOW().init();

        // Sticky Navbar
        $(window).scroll(function () {
            if ($(this).scrollTop() > 300) {
                $('.sticky-top').addClass('shadow-sm').css('top', '0px');
                $('.back-to-top').fadeIn('slow');
            } else {
                $('.sticky-top').removeClass('shadow-sm').css('top', '-100px');
                $('.back-to-top').fadeOut('slow');
            }
        });

        // Back to top button click action
        $('.back-to-top').click(function () {
            $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
            return false;
        });

        // Counter Up
        $('[data-toggle="counter-up"]').counterUp({
            delay: 10,
            time: 2000
        });

        // Header carousel
        $(".header-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            loop: true,
            nav: false,
            dots: true,
            items: 1,
            dotsData: true,
        });

        // Video Autoplay Fallback
        const videoElement = document.getElementById('background-video');
        if (videoElement) {
            videoElement.play().catch(function (error) {
                console.warn("Autoplay prevented or failed. Showing controls for manual play.");
                videoElement.controls = true; // Show controls for manual play
            });
        }

        // Testimonials carousel
        $(".testimonial-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1000,
            center: true,
            dots: false,
            loop: true,
            nav: true,
            navText: [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsive: {
                0: { items: 1 },
                768: { items: 2 }
            }
        });

        // Portfolio isotope and filter
        var portfolioIsotope = $('.portfolio-container').isotope({
            itemSelector: '.portfolio-item',
            layoutMode: 'fitRows'
        });
        $('#portfolio-flters li').on('click', function () {
            $("#portfolio-flters li").removeClass('active');
            $(this).addClass('active');
            portfolioIsotope.isotope({ filter: $(this).data('filter') });
        });
    });

})(jQuery);
