document.getElementById('menuIcon').addEventListener('click', function() {
    
    var menuContainer = document.querySelector('.menu-link-container');
    if (menuContainer.style.display === 'block') {
        menuContainer.style.display = 'none';
    } else {
        menuContainer.style.display = 'block';
    }

});