function showCreateFolderPanel() {
    document.getElementById("create-folder-modal").style.display = "block";
}

document.getElementById("cancel-btn").addEventListener("click", function() {
    document.getElementById("create-folder-modal").style.display = "none";
});

document.addEventListener('DOMContentLoaded', function () {
    const ellipsisIcons = document.querySelectorAll('.ellipsis-icon');
    ellipsisIcons.forEach(function (icon) {
        icon.addEventListener('click', function (event) {
            const popup = event.target.nextElementSibling;
            popup.classList.toggle('show');
        });
    });
});
/*
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

