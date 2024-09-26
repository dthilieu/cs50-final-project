document.getElementById("nextButton").addEventListener("click", function() {
    const spinner = document.getElementById("loadingSpinner");
    const image = document.getElementById("quoteImage");

    // Show the spinner
    spinner.style.display = "block";

    // Add class to darken image
    image.classList.add("loading"); 

    // Generate new random quote image
    fetch("/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Cannot fetch new image quote")
            }

            // Add timestamp to avoid caching
            image.src = "static/images/quote_image.jpg?" + new Date().getTime();
        })
        .catch(error => {
            console.error("There was a problem with generating new quote image", error);
        })
        .finally(() => {
            // Hide the spinner after the fetch completes
            spinner.style.display = "none";

            // Remove the darkening effect
            image.classList.remove("loading"); 
        });
});