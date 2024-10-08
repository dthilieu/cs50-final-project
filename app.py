from flask import Flask, render_template, session, jsonify, request
from flask_session import Session
from helpers import get_random_quote, get_random_image, write_quote_on_image, apology, clear_saved_quotes_folder
import time, os, shutil
import copy

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Required to use sessions
app.secret_key = 'supersecretkey'  

@app.route("/")
def index():
    """
    # Check if the request is an AJAX (fetch) request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        # Only clear session during a full page load, not for fetch requests
        session.clear()
        
        # Path to the previous quote image
        previous_image_path = os.path.join(app.static_folder, 'images', 'previous_quote_image.jpg')

        # Path to the current quote image
        current_image_path = os.path.join(app.static_folder, 'images', 'quote_image.jpg')

        # Check if the file exists and delete it to reset
        for image_path in [previous_image_path, current_image_path]:
            if os.path.exists(image_path):
                os.remove(image_path)
    """
  
    # Check if the request is an AJAX (fetch) request
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        # Only clear saved_quotes session during a full page load, not for fetch requests
         session.pop('saved_quotes', None)
         clear_saved_quotes_folder(app.static_folder)

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

"""
@app.route("/save", methods=["POST"])
def save_quote_image():
    # Save current displayed quote image information {quote, author, image_id}

    # Get the JSON data from the frontend
    data = request.json  

    # Get whether the current image is "current" or "previous"
    source = data.get('source')  
    
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
"""

@app.route("/save", methods=["POST"])
def save_quote_image():
    """
    Save current displayed quote image information {quote, author, image_id}
    """
    # Get the JSON data from the frontend
    data = request.json  

    # Get whether the current image is "current" or "previous"
    source = data.get('source')  
    
    # Determine which quote is being saved based on source
    if source == 'current':
        image_path = 'static/images/quote_image.jpg'
    else:
        image_path = 'static/images/previous_quote_image.jpg'

    # Generate a timestamp ID for the new saved image
    timestamp_id = int(time.time())
    saved_image_path = f'static/images/saved-quotes/saved_quote_{timestamp_id}.jpg'

    # Copy the current image to the new saved image
    shutil.copy(image_path, saved_image_path)

    # Initialize saved_quotes in the session if it doesn't exist
    if 'saved_quotes' not in session:
        # Initialize the list if not present
        session['saved_quotes'] = []  
    
    # Add the quote to the saved_quotes list
    session['saved_quotes'].append(f'saved_quote_{timestamp_id}.jpg')

    return jsonify({'message': 'Quote saved successfully!'}), 200


@app.route("/saved-quotes")
def saved_quotes():
    """
    Get a list of current saved quotes and display using HTML
    """
    # Ensure that saved_quotes list is exist incase of empty saved quotes
    saved_quotes = session.get('saved_quotes', [])
    return render_template("saved_quotes.html", saved_quotes=saved_quotes)

if __name__ == "__main__":
    app.run(debug=True)