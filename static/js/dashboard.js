const savedQuotes = document.getElementById("savedQuotes");

// Saved quotes button clicked
savedQuotes.addEventListener("click", function() {
    // Redirect to the /saved-quotes route
    window.location.href = "/saved-quotes";
});