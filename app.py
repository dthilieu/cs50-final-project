from flask import Flask, render_template
from helpers import get_random_quote, get_random_image, write_quote_on_image, apology

# Configure application
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)