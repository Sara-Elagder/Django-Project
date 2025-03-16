document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const sidebar = document.getElementById("sidebar");
    const container = document.querySelector(".container");

    menuToggle.addEventListener("click", function () {
        sidebar.classList.toggle("show");
        if (sidebar.classList.contains("show")) {
            document.querySelector(".container").style.marginLeft = "200px";
            document.querySelector(".pagination-container").style.left = "200px";
        } else {
            document.querySelector(".container").style.marginLeft = "50px";
            document.querySelector(".pagination-container").style.left = "50px";
        }
    });
});
