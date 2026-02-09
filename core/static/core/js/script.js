document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // Dark Mode Toggle Logic
    // ==========================================
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            if(toggleSwitch) toggleSwitch.checked = true;
        }
    }

    function switchTheme(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    }

    if (toggleSwitch) {
        toggleSwitch.addEventListener('change', switchTheme);
    }

    // ==========================================
    // Landing Page Orchestration
    // ==========================================
    const landingPage = document.getElementById('landing-page');
    const logo = document.getElementById('logo-image');
    const welcomeText = document.querySelector('.welcome-text');
    const loadingScreen = document.getElementById('loading-screen');
    const mainContent = document.getElementById('main-content');
    const body = document.body;

    // Only run if elements exist (e.g., on index page)
    if (landingPage && loadingScreen && mainContent) {
        
        // CHECK SESSION STORAGE: Has the user seen the intro?
        if (sessionStorage.getItem('introShown')) {
            // YES: Skip animation entirely
            landingPage.style.display = 'none';
            loadingScreen.style.display = 'none';
            mainContent.style.display = 'block';
            body.style.overflow = 'auto';
        } else {
            // NO: Show animation (Initial state is already set in HTML/CSS)
            body.style.overflow = 'hidden';

            landingPage.addEventListener('click', () => {
                // 1. Camera Zoom INTO Logo Effect
                if(logo) logo.classList.add('zoom-effect');
                landingPage.classList.add('landing-fade');
                
                // Fade out welcome text quickly
                if(welcomeText) {
                    welcomeText.style.transition = 'opacity 0.3s ease';
                    welcomeText.style.opacity = '0';
                }

                // 2. Wait for zoom animation to complete (1.5s)
                setTimeout(() => {
                    // Switch to Loading Screen
                    landingPage.style.display = 'none';
                    loadingScreen.style.display = 'flex'; 
                    
                    // Fade in loader
                    setTimeout(() => {
                        loadingScreen.classList.add('visible');
                    }, 50);

                    // 3. Loading Time then Reveal Main Content
                    setTimeout(() => {
                        loadingScreen.style.opacity = '0';
                        setTimeout(() => {
                            loadingScreen.style.display = 'none';
                            // Show main content and restore scrolling
                            mainContent.style.display = 'block';
                            body.style.overflow = 'auto';
                            
                            // MARK AS SEEN: Set session storage flag
                            sessionStorage.setItem('introShown', 'true');
                            
                        }, 500); // Wait for fade out
                    }, 2000); // 2 seconds loading time

                }, 1500); // Match CSS animation duration
            });
        }
    }

    // ==========================================
    // Scroll Animations (Intersection Observer)
    // ==========================================
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target); // Only animate once
            }
        });
    }, {
        root: null,
        threshold: 0.15, // Trigger when 15% visible
        rootMargin: "0px 0px -50px 0px"
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // ==========================================
    // Gallery Carousel Logic
    // ==========================================
    const carouselContainer = document.getElementById('main-carousel');
    console.log("Carousel Container found:", !!carouselContainer);

    if (carouselContainer) {
        const slides = carouselContainer.querySelectorAll('.carousel-slide');
        const dots = carouselContainer.querySelectorAll('.dot');
        const prevBtn = carouselContainer.querySelector('.prev');
        const nextBtn = carouselContainer.querySelector('.next');
        let currentSlide = 0;
        let slideInterval;

        function showSlide(index) {
            if (slides.length === 0) return;
            
            // Remove active from current
            slides[currentSlide].classList.remove('active');
            if (dots[currentSlide]) dots[currentSlide].classList.remove('active');
            
            // Set new index with wrapping
            currentSlide = (index + slides.length) % slides.length;
            
            // Add active to new
            slides[currentSlide].classList.add('active');
            if (dots[currentSlide]) dots[currentSlide].classList.add('active');
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function prevSlide() {
            showSlide(currentSlide - 1);
        }

        function startAutoPlay() {
            stopAutoPlay(); // Safety clear
            slideInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoPlay() {
            if (slideInterval) clearInterval(slideInterval);
        }

        // Event Listeners
        if (nextBtn) {
            nextBtn.onclick = () => {
                nextSlide();
                startAutoPlay();
            };
        }

        if (prevBtn) {
            prevBtn.onclick = () => {
                prevSlide();
                startAutoPlay();
            };
        }

        dots.forEach((dot, idx) => {
            dot.onclick = () => {
                showSlide(idx);
                startAutoPlay();
            };
        });

        // Pause on hover
        carouselContainer.onmouseenter = stopAutoPlay;
        carouselContainer.onmouseleave = startAutoPlay;

        // Initial Start
        startAutoPlay();
    }
});
