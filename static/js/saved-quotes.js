// Event listener for heart button click
document.querySelectorAll(".heart-button").forEach(button => {
    button.addEventListener("click", function() {
        // Get the image_id from data attribute
        const image_id = button.getAttribute("image_id");

        // Toggle the "clicked" class to change heart icon apperance
        button.classList.toggle("clicked");

        if (button.classList.contains("clicked")) {
            // Send an AJAX request to the backend to remove quote from saved quotes
            fetch("/remove-saved-quote", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                // Send the quote image_id
                body: JSON.stringify({ image_id: image_id })
            })
                .then((response) =>response.json())
                .then((data) => {
                    if (data.message) {
                        console.log(data.message);
                    } else {
                        console.error(data.error || "Error remove quote");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        } else {
            // Re-save quote image to saved quote image list in database
            const image = document.getElementById(image_id)
            fetch("/save", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    // Custom header
                    "X-Requested-With": "Fetch"  
                },
                body: JSON.stringify({ image_id: image_id, image_path: image.src }
                )
            })
                .then((response) =>response.json())
                .then((data) => {
                    if (data.message) {
                        console.log(data.message);
                    } else {
                        console.error(data.error || "Error remove quote");
                    }
                })
                .catch((error) => {
                    console.error("Error:", error);
                });
        }

        
    });
});