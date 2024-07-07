document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links-container a');
    const firstLink = document.querySelector('.home-link');
    const icons = document.querySelectorAll('.nav-links-container a i');
    const firstIcon = document.querySelector('.first-icon');
    const firstLinkText = document.querySelector('.home-text');
    const linksText = document.querySelectorAll('.nav-links-container a span');

    // Add hover effect to all links except the first one
    for (let i = 1; i < navLinks.length; i++) {
        navLinks[i].addEventListener('mouseover', function() {
            firstLink.classList.remove('link-hovered');
            navLinks[i].classList.add('link-hovered');
            firstIcon.classList.remove('icon-hovered');
            icons[i].classList.add('icon-hovered');
            firstLinkText.classList.remove('link-text-hovered');
            linksText[i].classList.add('link-text-hovered');
        });
        navLinks[i].addEventListener('mouseout', function() {
            firstLink.classList.add('link-hovered');
            navLinks[i].classList.remove('link-hovered');
            firstIcon.classList.add('icon-hovered');
            icons[i].classList.remove('icon-hovered');
            firstLinkText.classList.add('link-text-hovered');
            linksText[i].classList.remove('link-text-hovered');
        });
    }
});

document.getElementById('addFolderIcon').addEventListener("click", function() {
    document.getElementById("create-folder-modal").style.display = "block";
});

document.getElementById("cancel-btn").addEventListener("click", function() {
    document.getElementById("create-folder-modal").style.display = "none";
});

document.querySelector('.folder-container-instance').addEventListener('click', function() {
    document.getElementById('payment-link').click();
});

