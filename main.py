import spidev as SPI
import logging
import ST7789
import subprocess
import time
from PIL import Image, ImageDraw, ImageFont
import textwrap
import requests
import os
import json

import fortune

# Initialize the display
disp = ST7789.ST7789()
disp.Init()
disp.clear()
disp.bl_DutyCycle(50)

# Create blank image for drawing
image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
draw = ImageDraw.Draw(image1)

# Create the fonts
Font1 = ImageFont.truetype("Font02.ttf", 24)
Font1_medium = ImageFont.truetype("Font02.ttf", 28)
Font1_large = ImageFont.truetype("Font02.ttf", 32)


########################################################
########      ADD YOUR VERUS WALLET             ########
########################################################
wallet_address = "VERUS_WALLET_ADDRESS"

def get_verus_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=verus-coin&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("verus-coin").get("usd")
    except requests.RequestException as e:
        print(f"Error fetching Verus coin price: {e}")
        return None

def fetch_verus_data():
    price = get_verus_price()
    url = 'https://luckpool.net/verus/miner/' + wallet_address
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        data['price'] = price
        data['timestamp'] = time.time()
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_verus_data():
    data = fetch_verus_data()
    if data is None:
        print("No data available.")
        return
    
    price = data.get('price', 'N/A')
    hashrateString = data.get("hashrateString", 'N/A')
    shares = data.get("shares", 'N/A')
    estimatedLuck = data.get("estimatedLuck", 'N/A')
    balance = data.get("balance", 'N/A')
    paid = data.get("paid", 'N/A')
    workers = data.get("workers", [])
    num_workers = len(workers)
    
    draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
    draw.text((5, 0), f"VRSC: ${price:.2f} USD", fill="ORANGE", font=Font1_large)
    draw.text((5, 40), f"Hashrate: {hashrateString}/s", fill="CYAN", font=Font1_medium)
    draw.text((5, 80), f"Workers: {num_workers}", fill="BLUE", font=Font1)
    draw.text((5, 110), f"Shares: {shares:.2f}", fill="PINK", font=Font1)
    draw.text((5, 140), f"Luck: {estimatedLuck}", fill="YELLOW", font=Font1)
    draw.text((5, 180), f"Now: {balance:.2f} VRSC", fill="GRAY", font=Font1)
    draw.text((5, 210), f"Paid: {paid:.2f} VRSC", fill="GREEN", font=Font1)
    disp.ShowImage(image1)    

logging.basicConfig(level=logging.DEBUG)

def check_buttons():
    if disp.digital_read(disp.GPIO_KEY_UP_PIN) != 0:  # UP
        logging.info("Up button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        draw.text((100, 100), "UP", fill="RED", font=Font1)
        disp.ShowImage(image1)
        time.sleep(0.3)  # Debounce delay
        
    if disp.digital_read(disp.GPIO_KEY_DOWN_PIN) != 0:  # DOWN
        logging.info("Down button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        draw.text((90, 100), "DOWN", fill="RED", font=Font1)
        disp.ShowImage(image1)
        time.sleep(0.3)  # Debounce delay
        
    if disp.digital_read(disp.GPIO_KEY_LEFT_PIN) != 0:  # LEFT
        logging.info("Left button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        fortune.display_fortune(draw, Font1, disp, image1)
        time.sleep(0.3)  # Debounce delay
        
    if disp.digital_read(disp.GPIO_KEY_RIGHT_PIN) != 0:  # RIGHT
        logging.info("Right button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        fortune.display_fortune(draw, Font1, disp, image1)
        time.sleep(0.3)  # Debounce delay
        
    if disp.digital_read(disp.GPIO_KEY_PRESS_PIN) != 0:  # CENTER
        logging.info("Center button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        draw.text((100, 100), "CENTER", fill="RED", font=Font1)
        disp.ShowImage(image1)
        time.sleep(0.3)  # Debounce delay

    if disp.digital_read(disp.GPIO_KEY1_PIN) != 0:  # KEY 1
        logging.info("KEY1 button pressed")
        display_verus_data()

    if disp.digital_read(disp.GPIO_KEY2_PIN) != 0:  # KEY 2
        logging.info("KEY2 button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        disp.ShowImage(image1)
        time.sleep(0.3)  # Debounce delay
        
    if disp.digital_read(disp.GPIO_KEY3_PIN) != 0:  # KEY 3
        logging.info("KEY3 button pressed")
        draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
        disp.ShowImage(image1)
        time.sleep(0.3)  # Debounce delay

draw.rectangle([(0, 0), (240, 240)], fill="BLACK")
while True:
    check_buttons()
    time.sleep(0.1)  # Small delay to avoid excessive CPU usage
