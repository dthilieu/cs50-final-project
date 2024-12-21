const navigateButton = document.getElementById("navigateButton");

// Navigate button clicked
navigateButton.addEventListener("click", function() {
    // If navigate button is Saved Quotes
    if (navigateButton.textContent.trim() === "Saved Quotes") {
        // Redirect to the /saved-quotes route
        window.location.href = "/saved-quotes"; 
    } 
    // If navigate button is Homepage
    else if (navigateButton.textContent.trim() === "Generate Quotes") {
        history.back();
    }
});