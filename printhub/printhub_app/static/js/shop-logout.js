document.getElementById('profileIcon').addEventListener('click', function() {
    var logoutContainer = document.querySelector('.logout-container');
    if (logoutContainer.style.display === 'block') {
        logoutContainer.style.display = 'none';
    } else {
        logoutContainer.style.display = 'block';
    }
});