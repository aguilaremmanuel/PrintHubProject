document.getElementById("cancel-btn").addEventListener("click", function() {
    document.getElementById("join-shop-modal").style.display = "none";
});

document.getElementById('join-shop-btn').addEventListener('click', function() {
    // Step 3: Define the function to be executed when the event is triggered
    document.getElementById("join-shop-modal").style.display = "block";
});
