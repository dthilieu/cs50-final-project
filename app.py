from flask import Flask, render_template
from helpers import get_random_quote, get_random_image, write_quote_on_image

# Configure application
app = Flask(__name__)

@app.route("/")
def index():
    quote_data = get_random_quote()

    quote = quote_data[0]["q"]
    author = quote_data[0]["a"]

    photo = get_random_image()

    write_quote_on_image(quote, author, photo["urls"]["regular"])

    return render_template("index.html", quote=quote, author=author, photo=photo)
    # return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True)