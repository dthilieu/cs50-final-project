from flask import Flask, render_template, session, jsonify, request
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

    # If there is a current quote and image, store them as previous ones
    if 'current_quote' in session:
        session['previous_quote'] = session['current_quote']

    # Update the current quote and image in session
    session['current_quote'] = {
        'quote': quote,
        'author': author,
        'image_id': photo["id"]
    }

    # Make sure image response is 200 no error
    try:
        write_quote_on_image(quote, author, photo["urls"]["regular"])
        return render_template("index.html")
    except:
        # If error, show apology
        return apology(photo[0], photo[1])

@app.route("/save", methods=["POST"])
def save_quote_image():
    data = request.json  # Get the JSON data from the frontend
    source = data.get('source')  # Get whether the current image is "current" or "previous"
    
    # Determine which quote is being saved based on source
    if source == 'current':
        quote_to_save = session['current_quote']
    else:
        quote_to_save = session['previous_quote']

    # Save the quote in the session under 'saved_quotes'
    if 'saved_quotes' not in session:
        session['saved_quotes'] = []  # Initialize the list if not present

    # Add the quote to the saved_quotes list
    session['saved_quotes'].append(quote_to_save)

    return jsonify({'message': 'Quote saved successfully!'}), 200

if __name__ == "__main__":
    app.run(debug=True)