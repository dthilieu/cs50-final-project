import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from io import BytesIO
from flask import render_template
import shutil
import os

def get_random_quote():
    """Get any random quote from ZenQuotes API."""

    # ZenQuotes API
    url = "https://zenquotes.io/api/random"
    
    # Query API
    try:
        response = requests.get(url)
        return response.json()
    except:
        return None

def get_random_image():
    """Get image from Pexels API."""

    # Unsplash API Key
    ACCESS_KEY = 'FQeoaKtz5CjL1WV3qycCF8rncH-0MtcQ1CWo8X_y0Jc'

    # Endpoint for random photo
    url = 'https://api.unsplash.com/photos/random'

    # Authorization Header
    headers = {"Authorization": f"Client-ID {ACCESS_KEY}"}

    params = {
        "query": "nature",
        "orientation": "landscape"
    }

    # Make the request
    response = requests.get(url, headers=headers, params=params)

    # Parse the response
    if response.status_code == 200:
        image = response.json()
        return image
    else:
        return "Too much request, slow down!", response.status_code

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

def write_quote_on_image(quote, author, image_url):
    """Write quote on image."""

    def getsize(font, text):
        """
        Get size of text with given font size (width and height)
        """
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top
    
    def draw_text_wrapped(draw, font_size, position, max_width):
        """
        Draw text on the image with wrapping based on the max_width.
        """
        lines = []
        words = quote.split()
        current_line = ''

        # Load font for quote
        font_path = "static/fonts/ComicNeue-Bold.ttf"
        font = ImageFont.truetype(font_path, font_size)
        
        # Seperate quote into lines with length <= max_width
        for word in words:
            test_line = f'{current_line} {word}'.strip()
            quote_width = getsize(font, test_line)[0]
            
            if quote_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        # Add the last line
        lines.append(current_line) 
        
        # Draw each line on the image
        y_position = position[1]
        for line in lines:
            draw.text((position[0], y_position), line, font=font, fill="white")

            # Move to the next line
            y_position += getsize(font, line)[1] * 1.5  
        
        # Load font for author
        font_path = "static/fonts/ComicNeue-Italic.ttf"
        font = ImageFont.truetype(font_path, font_size - 20)

        # Draw author on the image
        author_width = getsize(font, author)[0]
        author_x_position = max_width - author_width
        draw.text((author_x_position, y_position), author, font=font, fill="white")

    # Fetch the image data from url
    image_response = requests.get(image_url)

    # Open image content as file-like object to use Pillow library
    img = Image.open(BytesIO(image_response.content))

    # Adjust the brightness
    enhancer = ImageEnhance.Brightness(img)
    dark_img = enhancer.enhance(0.5)

    # Use draw function
    draw = ImageDraw.Draw(dark_img)

    # Define quote first line position
    quote_position = (100, 100)

    # Image width to wrap the text, considering margins
    max_width = img.width - (1.6 * quote_position[0] )

    # Length of quote
    quote_length = len(quote.split())

    # Different font size based on length of quote
    if quote_length < 15:
        font_size = 80
    elif quote_length > 25:
        font_size = 60
    else:
        font_size = 70

    # Draw wrapped quote and author on the image
    draw_text_wrapped(draw, font_size, quote_position, max_width)

    # Image path
    current_image_path = 'static/images/quote_image.jpg'
    previous_image_path = 'static/images/previous_quote_image.jpg'

    # Check if current image exists before copying
    if os.path.exists(current_image_path):
        # Use shutil to copy the current image to the previous image location
        import shutil
        shutil.copy(current_image_path, previous_image_path)

    # Save the modified image
    dark_img.save("static/images/quote_image.jpg")





