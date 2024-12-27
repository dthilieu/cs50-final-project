const spinner = document.getElementById("loadingSpinner");
const image = document.getElementById("quoteImage");
const imageContainer = document.getElementById("imageContainer");

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
        fetch("/", {
            method: "GET",
            // Ensure header is set
            headers: {
                "X-Requested-With": "XMLHttpRequest"  
            }
        })
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

    // Update the data-source attribute to "current"
    imageContainer.setAttribute("data-source", "current");
});

// Previous button clicked
document.getElementById("previousButton").addEventListener("click", function() {
    // Previous image path
    const previousImagePath = '/static/images/previous_quote_image.jpg';

    // Check if the image exists using fetch with HEAD method
    fetch(previousImagePath, { method: 'HEAD' })
        .then(response => {
            if (response.ok) {
                // Image exists, so display it
                console.log("Previous image exists!");

                // Change source of image to previous one
                image.src = "static/images/previous_quote_image.jpg?" + new Date().getTime();

                // Update the data-source attribute to "previous"
                imageContainer.setAttribute("data-source", "previous");
            } else {
                // Image does not exist, handle this case
                console.log("Previous image does not exist.");
                alert("No previous quote available.");
            }
        })
        .catch(error => {
            console.log("Error checking previous image:", error);
        });
});

// Save button clicked
document.getElementById("saveButton").addEventListener("click", function() {
    // Get the source of the displayed image (either 'current' or 'previous')
    const source = imageContainer.getAttribute('data-source');

    // Fetch data to "/save" route
    fetch("/save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ source: source })  // Send the source in the request
    })
    .then(response => {
        if (response.status === 401) {
            // User is not logged in, show login prompt
            showLoginPromt();
        } else if (response.ok) {
            // User is logged in, proceed with save
            saveQuote();
        }
    })
    .catch( error => {
        console.error("Error:", error)
    });
});

// Prompt to redirect user to login 
function showLoginPromt() {
    const confirmLogin = confirm("You need to log in to save quotes. Do you want to log in now? ");
    if (confirmLogin) {
        // Redirect to login page
        window.location.href = "/login"
    }
}

// Function to handle the save quote proccess
function saveQuote() {
    // Darken image
    image.style.filter = "brightness(50%)";

    // Trigger the "Saved!" message animation
    savedMessage.style.opacity = 1;
    savedMessage.style.animation = 'fadeInOut 1.5s ease forwards';

    // After the animation
    setTimeout(() => {
        // Remove darkening
        image.style.filter = "brightness(100%)";

        // Reset opacity and animation for the "Saved!" message
        // Reset opacity
        savedMessage.style.opacity = 0;  

        // Reset animation
        savedMessage.style.animation = 'none';  

        // Force reflow to reset the animation
        savedMessage.offsetHeight;  

        // Matches the duration of the animation
    }, 1500);  
}