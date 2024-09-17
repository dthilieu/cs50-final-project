import requests
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
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

    def getsize(font, text):
        left, top, right, bottom = font.getbbox(text)
        return right - left, bottom - top
    
    def draw_text_wrapped(draw, text, font, position, max_width):
        """
        Draw text on the image with wrapping based on the max_width.
        """
        lines = []
        words = text.split()
        current_line = ''
        
        for word in words:
            test_line = f'{current_line} {word}'.strip()
            text_width = getsize(font, test_line)[0]
            
            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        lines.append(current_line)  # Add the last line
        
        # Draw each line on the image
        y_position = position[1]
        for line in lines:
            draw.text((position[0], y_position), line, font=font, fill="white")
            y_position += getsize(font, line)[1]  # Move to the next line

    # Fetch the image data from url
    image_response = requests.get(image_url)

    # Open image content as file-like object to use Pillow library
    img = Image.open(BytesIO(image_response.content))

    # Adjust the brightness
    enhancer = ImageEnhance.Brightness(img)
    dark_img = enhancer.enhance(0.5)

    # Use draw function
    draw = ImageDraw.Draw(dark_img)

    # Load font 
    font_size = 48
    font = ImageFont.truetype("PlayfairDisplay-Bold.ttf", font_size)

    # Define text position and color
    quote_position = (50, 50)
    author_position = (200, 250)
    text_color = (255, 255, 255) # White color

    # Image width to wrap the text, considering margins
    max_width = img.width - 2 * quote_position[0]

    # Draw wrapped quote on the image
    draw_text_wrapped(draw, quote, font, quote_position, max_width)

    # Draw author on the image
    draw.text(author_position, author, font=font, fill=text_color)

    # Save the modified image
    dark_img.save("static/images/image_with_quote.jpg")





