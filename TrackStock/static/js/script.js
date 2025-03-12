document.addEventListener("DOMContentLoaded", function () {
    let navbarToggler = document.querySelector(".navbar-toggler");
    let sidebar = document.querySelector(".sidebar");
    let content = document.querySelector(".content");

    navbarToggler.addEventListener("click", function () {
        sidebar.classList.toggle("menu-open");
        content.classList.toggle("menu-open");
    });
   });
