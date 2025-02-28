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

        // Initiate WOW.js (Check if WOW is available)
        if (typeof WOW !== "undefined") {
            new WOW().init();
        } else {
            console.warn("WOW.js is not loaded.");
        }

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

        // Counter Up (Check if counterUp plugin is loaded)
        if ($.fn.counterUp) {
            $(".counter").counterUp({
                delay: 10,
                time: 2000
            });
        } else {
            console.error("counterUp plugin is not loaded.");
        }

        // Header carousel (Check if Owl Carousel is loaded)
        if ($.fn.owlCarousel) {
            $(".header-carousel").owlCarousel({
                autoplay: true,
                smartSpeed: 1500,
                loop: true,
                nav: false,
                dots: true,
                items: 1,
                dotsData: true,
            });

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
        } else {
            console.error("Owl Carousel plugin is not loaded.");
        }

        // Video Autoplay Fallback
        const videoElement = document.getElementById('background-video');
        if (videoElement) {
            videoElement.play().catch(function (error) {
                console.warn("Autoplay prevented or failed. Showing controls for manual play.");
                videoElement.controls = true;
            });
        }

        // Portfolio isotope and filter (Check if Isotope is loaded)
        if ($.fn.isotope) {
            var portfolioIsotope = $('.portfolio-container').isotope({
                itemSelector: '.portfolio-item',
                layoutMode: 'fitRows'
            });
            $('#portfolio-flters li').on('click', function () {
                $("#portfolio-flters li").removeClass('active');
                $(this).addClass('active');
                portfolioIsotope.isotope({ filter: $(this).data('filter') });
            });
        } else {
            console.error("Isotope plugin is not loaded.");
        }
    });

})(jQuery);
