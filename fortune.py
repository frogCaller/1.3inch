import spidev as SPI
import logging
import ST7789
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap


def get_fortune():
    try:
        # Run the 'fortune' command and capture the output
        result = subprocess.run(['fortune'], stdout=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve fortune: {e}"

def display_fortune(draw, font, disp, image):
    fortune = get_fortune()

    # Clear the display
    draw.rectangle([(0, 0), (240, 240)], fill="BLACK")

    # Wrap the text to fit within the display width
    wrapped_text = textwrap.fill(fortune, width=23)  # Adjust width as needed

    # Display the fortune message
    y = 3
    for line in wrapped_text.split('\n'):
        draw.text((3, y), line, fill="WHITE", font=font)
        y += font.getsize(line)[1] + 3
        if y > 240 - font.getsize(line)[1]:  # If results overflow the screen, break
            break
    # Show the image with the text
    disp.ShowImage(image)
