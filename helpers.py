import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

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
        return None


def write_quote_on_image(quote, author, image_url):
    """Write quote on image."""

    # Fetch the image data from url
    image_response = requests.get(image_url)

    # Open image content as file-like object to use Pillow library
    img = Image.open(BytesIO(image_response.content))

    # Use draw function
    draw = ImageDraw.Draw(img)

    # Load font 
    font_size = 48
    font = ImageFont.truetype("PlayfairDisplay-Regular.ttf", font_size)

    # Define text position and color
    quote_position = (50, 50)
    author_position = (200, 150)
    text_color = (255, 255, 255) # White color

    # Draw quote on the image
    draw.text(quote_position, quote, font=font, fill=text_color)

    # Draw author on the image
    draw.text(author_position, author, font=font, fill=text_color)

    # Save the modified image
    img.save("static/images/image_with_quote.jpg")





