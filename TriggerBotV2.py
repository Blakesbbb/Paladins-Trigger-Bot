import time
import mss
import numpy as np
from pynput.mouse import Controller, Button
from pynput import keyboard
from threading import Thread
import random
import tkinter as tk
from PIL import Image


# Global variable to keep track of the overlay status
overlay_status = "OFF"

# Function to create a transparent overlay on the screen
def create_overlay():
    global overlay_status
    # Create a top-level window
    overlay = tk.Tk()
    overlay.title("Trigger Bot")

    # Set the position and size of the window
    overlay.geometry("100x50+10+10")
    # Make the window's background transparent
    overlay.attributes("-transparentcolor", "white")
    # Create a label with the specified text
    label = tk.Label(overlay, text=overlay_status, bg="white", font=("Helvetica", 20))
    label.pack(expand=True, fill="both")
    # Remove the title bar
    overlay.overrideredirect(True)
    # Keep the window always on top
    overlay.attributes("-topmost", True)

    # Function to update the text of the overlay label
    def update_overlay():
        nonlocal label
        label.config(text=overlay_status)
        # Schedule to be called after 100ms
        overlay.after(100, update_overlay)

    # Start the periodic update
    update_overlay()
    # Start the Tkinter event loop
    overlay.mainloop()

# Function to start the overlay in a separate thread
def start_overlay():
    """
    Starts the overlay in a separate thread.

    This function allows the main program to run concurrently with the overlay window.
    """
    overlay_thread = Thread(target=create_overlay)
    overlay_thread.daemon = True
    overlay_thread.start()

# Function to toggle the overlay status
def toggle_overlay_status(new_status):
    """
    Toggles the overlay status between 'ON' and 'OFF'.

    Args:
    - new_status: The new status to set for the overlay.
    """
    global overlay_status
    overlay_status = new_status

# Function to check if a pixel color matches the target colors within a deviation
def is_color_match(r, g, b, target_colors, deviation):
    for target in target_colors:
        if all(abs(c - t) <= deviation for c, t in zip((r, g, b), target)):
            return True
    return False

# Function to scan for the target colors in a screenshot
def scan_for_colors(sct_img, target_colors, color_deviation):
    img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            if is_color_match(r, g, b, target_colors, color_deviation):
                return True
    return False


# Function to toggle the bot on and off
def toggle_bot():
    global enabled, is_pressed, overlay_status
    if enabled:
        print("Disabled")

        toggle_overlay_status("OFF")
        enabled = False
        # If the button is pressed, release it
        if is_pressed:
            mouse.release(Button.left)
            is_pressed = False
    else:
        print("Enabled")
        toggle_overlay_status("ON")
        enabled = True
    time.sleep(0.2)

# Keyboard event handler to toggle the bot when '5' is pressed
def on_press(key):
    try:
        if key.char == '5':
            toggle_bot()
    except AttributeError:
        pass

if __name__ == '__main__':
    print('RUNNING')
    # Set up a listener for keyboard events
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    # Define the region, target colors, and color deviation, this is the middle 25x25 pixels of my 1920x1080 monitor
    # to find your values do (width and height / 2) - 25 for each width or height
    region = {'top': 515, 'left': 935, 'width': 25, 'height': 25}
    target_colors = [(253, 246, 85), (220, 164, 58), (222, 50, 59), (147, 37, 38)]
    # if you want more reactive increase the color deviation
    color_deviation = 17

    # Initialize the mouse controller and the bot's state
    mouse = Controller()
    enabled = False
    is_pressed = False

    # Start the overlay
    start_overlay()
    while True:
        if enabled:
            with mss.mss() as sct:
                # Define the screen region to capture
                monitor = {"top": region["top"], "left": region["left"], "width": region["width"],
                           "height": region["height"]}
                sct_img = sct.grab(monitor)
                # Scan the captured image for target colors
                is_color_matched = scan_for_colors(sct_img, target_colors, color_deviation)

            # firing
            if is_color_matched:
                if not is_pressed:
                    number = random.uniform(0.01, 0.05)
                    time.sleep(number)
                    mouse.press(Button.left)
                    is_pressed = True
            # no longer firing
            elif is_pressed:
                mouse.release(Button.left)
                is_pressed = False

            # delay before seeing if still firing
            if is_pressed:
                number = random.uniform(0.1, 0.3)
                time.sleep(number)
