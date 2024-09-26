from flask import Flask, render_template, session, jsonify
from helpers import get_random_quote, get_random_image, write_quote_on_image, apology
import time, os, shutil

# Configure application
app = Flask(__name__)

# Required to use sessions
app.secret_key = 'supersecretkey'  

@app.route("/")
def index():
    # Get random quote from API
    quote_data = get_random_quote()

    # Change quote and author format
    quote = '"' + quote_data[0]["q"].strip() + '"'
    author = "-" + quote_data[0]["a"]

    # Get random photo from API
    photo = get_random_image()

    # Make sure image response is 200 no error
    try:
        write_quote_on_image(quote, author, photo["urls"]["regular"])
        return render_template("index.html")
    except:
        # If error, show apology
        return apology(photo[0], photo[1])

@app.route("/save", methods=["POST"])
def save_quote_image():
    current_image_path = 'static/images/quote_image.jpg'

    # Generate a timestamp ID for the new saved image
    timestamp_id = int(time.time())
    saved_image_path = f'static/images/saved_quote_{timestamp_id}.jpg'

    # Copy the current image to the new saved image
    shutil.copy(current_image_path, saved_image_path)

    # Store the saved image filename in the session list
    if 'saved_quotes' not in session:
        # Initialize if not present
        session['saved_quotes'] = []  

    session['saved_quotes'].append(f'saved_quote_{timestamp_id}.jpg')

    return jsonify({"message": f"Quote image saved: {saved_image_path}"}), 200


if __name__ == "__main__":
    app.run(debug=True)