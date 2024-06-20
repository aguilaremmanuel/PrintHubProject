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

/*
function showCreateFolderPanel() {
    document.getElementById("create-folder-modal").style.display = "block";
}
*/

document.getElementById("cancel-btn").addEventListener("click", function() {
    document.getElementById("create-folder-modal").style.display = "none";
});





/*
document.addEventListener('DOMContentLoaded', function () {
    const ellipsisIcons = document.querySelectorAll('.ellipsis-icon');
    ellipsisIcons.forEach(function (icon) {
        icon.addEventListener('click', function (event) {
            const popup = event.target.nextElementSibling;
            popup.classList.toggle('show');
        });
    });
});

document.querySelectorAll('.folder-state').forEach(function(element) {
    element.addEventListener('click', function() {
        const folderId = this.getAttribute('data-id');
        const newState = this.getAttribute('data-state');
        fetch(`/change_folder_state/${folderId}/${newState}/`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => response.json())
          .then(data => {
              if (data.success) {
                  location.reload(); // Reload the page to reflect changes
              } else {
                  alert('Failed to change folder state.');
              }
          });
    });
});
*/

