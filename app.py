from cs50 import SQL
from flask import Flask, flash, redirect, render_template, session, jsonify, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import get_random_quote, get_random_image, write_quote_on_image, clear_saved_quotes_folder
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

    # Retrieve and clear intent_quote if any
    intent_quote = session.pop("intent_quote", None)
    if intent_quote:
        # Render the stored intent quote
        return render_template("index.html")

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
        flash("Cannot generate quote! Please come back later.")
        return redirect("/login")

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
        if (not username) or (not password) or (not confirmation):
            flash("Missing required information!")
            return redirect("/register")
        elif password != confirmation:
            flash("The passwords do not match!")
            return redirect("/register")
        
        # Check if the username already exists
        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))
        except ValueError:
            flash("The username already exists!")
            return redirect("/register")
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Record flash message
        flash("Account created successfully! You can now log in.")

        # Redirect user to home page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in
    """

    session.pop("user_id", None)

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username and password was submitted
        if not request.form.get("username") or not request.form.get("password"):
            flash("Missing Username and/ or Password!")
            return redirect("/login")
        
        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
            )
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Invalid username and/ or password!")
            return redirect("/login")
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

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

    flash("Logged out!")

    # Redirect user to homepage
    return redirect("/login")

@app.route("/save", methods=["POST"])
def save_quote_image():
    """
    Save current displayed quote image information {image_id, image_path}
    """

    # Check if any user logged in
    if "user_id" not in session:
        # If not, return error code unauthorized
        return jsonify({"error": "Not logged in"}), 401
    
    # Get the JSON data from the frontend
    data = request.json

    # Get user_id from session
    user_id = session["user_id"]

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

    # Copy the current image to the new saved image
    shutil.copy(image_path, saved_image_path)

    # Save quote into the database
    db.execute("INSERT INTO saved_quotes (user_id, image_id, image_path) VALUES (?, ?, ?)",
               user_id, image_id, saved_image_path)

    return jsonify({'message': 'Quote saved successfully!'}), 200

@app.route("/get-saved-quotes")
def saved_quotes():
    """
    Get a list of current saved quotes and display using HTML
    """
    # Get saved quote list from database
    saved_quotes = db.execute("SELECT * FROM saved_quotes WHERE user_id = ?", session["user_id"])

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
    try:
        db.execute("DELETE FROM saved_quotes WHERE user_id=? AND image_id=?", 
               session["user_id"], image_id)

        return jsonify({"message": "Quote removed successfully!"}), 200
    except:
        return jsonify({"error": "No saved quotes found"}), 400

@app.route("/store-intent", methods=["POST"])
def store_intent():
    """
    Store intent quote before redirect to log in page from login modal.
    """
    # Get quote data from the request
    intent_quote = request.json  

    # Save it in the session
    session["intent_quote"] = intent_quote

    return jsonify({"message": "Intent stored successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)