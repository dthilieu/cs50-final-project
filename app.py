from cs50 import SQL
from flask import Flask, flash, redirect, render_template, session, jsonify, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_random_quote, get_random_image, write_quote_on_image, apology, clear_saved_quotes_folder
import time, os, shutil
import copy

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quote-generator.db")

# Required to use sessions
app.secret_key = 'supersecretkey'  

@app.route("/")
def index():
    """
    Show random generated quote
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

@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user
    """

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username= request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validate name and password
        if not username and not password:
            return apology("Missing Username and Password")
        elif not username:
            return apology("Missing Username")
        elif not password:
            return apology("Missing Password")

        # Validate password confirmation
        elif not confirmation:
            return apology("Missing Password Confirmation")
        elif password != confirmation:
            return apology("The passwords do not match")
        
        # Check if the username already exists
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))
        except ValueError:
            return apology("The username already exists")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Record flash message
        flash("Register!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in
    """

    # Forgt any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE usersname = ?", request.form.get("username")
            )
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/ or password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Record flash message
        flash("Log in!")

        # Redirect user to homepage
        return redirect("/")
    
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """
    Log user out
    """

    # Forget any user_id
    session.clear()

    # Redirect user to homepage
    return redirect("/")

@app.route("/save", methods=["POST"])
def save_quote_image():
    """
    Save current displayed quote image information {image_id, image_path}
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

    # Generate a timestamp ID as image_id for the new saved image
    image_id = int(time.time())
    saved_image_path = f'static/images/saved-quotes/saved_quote_{image_id}.jpg'

    # Initialize quote_to_save dictionary
    quote_to_save = {
        "image_id": image_id,
        "image_path": saved_image_path
        }


    # Copy the current image to the new saved image
    shutil.copy(image_path, saved_image_path)

    # Initialize saved_quotes in the session if it doesn't exist
    if 'saved_quotes' not in session:
        # Initialize the list if not present
        session['saved_quotes'] = []  
    
    # Add the quote to the saved_quotes list
    session['saved_quotes'].append(quote_to_save)

    return jsonify({'message': 'Quote saved successfully!'}), 200

@app.route("/saved-quotes")
def saved_quotes():
    """
    Get a list of current saved quotes and display using HTML
    """
    # Ensure that saved_quotes list is exist incase of empty saved quotes
    saved_quotes = session.get('saved_quotes', [])
    return render_template("saved_quotes.html", saved_quotes=saved_quotes)

@app.route("/remove-saved-quote", methods=["POST"])
def remove_quote():
    """
    Remove a saved quote from the list.
    Expects JSON data with "image_id" identifying the quote.
    """
    data = request.json
    image_id = data.get("image_id")

    # Check if the image_id exists
    if not image_id:
        return jsonify({"error": "Invalid request, missing image_id"}), 400
    
    # Remove the quote from saved_quotes
    if "saved_quotes" in session:
        session["saved_quotes"] = [quote for quote in session["saved_quotes"] if quote["image_id"] != image_id]
        session.modified = True

        return jsonify({"message": "Quote removed successfully!"}), 200
    
    return jsonify({"error": "No saved quotes found"}), 400


if __name__ == "__main__":
    app.run(debug=True)