document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.querySelector('.navbar-toggler');
    const sidebar = document.querySelector('.sidebar');
    const bodyOverlay = document.createElement('div');
    bodyOverlay.className = 'body-overlay';
    document.body.appendChild(bodyOverlay);

    toggleButton.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        bodyOverlay.classList.toggle('active');
    });

    bodyOverlay.addEventListener('click', function() {
        sidebar.classList.remove('active');
        bodyOverlay.classList.remove('active');
    });

    // Close sidebar on window resize if in mobile view
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            sidebar.classList.remove('active');
            bodyOverlay.classList.remove('active');
        }
    });
});
