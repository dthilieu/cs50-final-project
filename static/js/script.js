const spinner = document.getElementById("loadingSpinner");
const image = document.getElementById("quoteImage");

// Next button clicked
document.getElementById("nextButton").addEventListener("click", function() {

    // Check if current displayed image is previous_quote_image.jpg
    if (image.src.includes("static/images/previous_quote_image.jpg")) {
        // Add timestamp to avoid caching
        image.src = "static/images/quote_image.jpg?" + new Date().getTime();
    } else {
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
    }
});

// Previous button clicked
document.getElementById("previousButton").addEventListener("click", function() {
    // Change source of image to previous one
    image.src = "static/images/previous_quote_image.jpg?" + new Date().getTime();
});

// Save button clicked
document.getElementById("saveButton").addEventListener("click", function() {
    // Darken image
    image.style.filter = "brightness(50%";

    // Save current image
    fetch("/save", {method: "POST"})
    .then(response => response.json())
    .then(data => {
        // Log the success message
        console.log(data.message);

        // Trigger the "Saved!" message animation
        savedMessage.style.opacity = 1;
        savedMessage.style.animation = 'fadeInOut 1.5s ease forwards';

        // After the animation
        setTimeout(() => {
            // Remove darkening
            image.style.filter = "brightness(100%)";

            // Reset opacity and animation for the "Saved!" message
            savedMessage.style.opacity = 0;  // Reset opacity
            savedMessage.style.animation = 'none';  // Reset animation
            savedMessage.offsetHeight;  // Force reflow to reset the animation
        }, 1500);  // Matches the duration of the animation
    })
    .catch(error => {
        console.error("Error:", error);
    });
});