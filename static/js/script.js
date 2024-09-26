document.getElementById("nextButton").addEventListener("click", function() {
    fetch("/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Cannot fetch new image quote")
            }

            // Update image source to refresh it
            const image = document.getElementById("quoteImage");

            // Add timestamp to avoid caching
            image.src = "static/images/quote_image.jpg?" + new Date().getTime();
        })
        .catch(error => {
            console.error("There was a problem with generating new quote image", error);
        });
});