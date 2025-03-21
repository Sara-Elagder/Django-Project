document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.sidebar');
    const navbar = document.querySelector('.navbar');
    const mainContainer = document.querySelector('.main_container');
    const bodyOverlay = document.createElement('div');
    bodyOverlay.className = 'body-overlay';
    document.body.appendChild(bodyOverlay);

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        bodyOverlay.classList.toggle('active');
        navbar.classList.toggle('shifted');
        mainContainer.classList.toggle('shifted');
    }

    toggleButton.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        toggleSidebar();
    });

    bodyOverlay.addEventListener('click', function() {
        toggleSidebar();
    });

    // Close sidebar on window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('active');
            bodyOverlay.classList.remove('active');
            navbar.classList.remove('shifted');
            mainContainer.classList.remove('shifted');
        }
    });
});
