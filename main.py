import numpy as np
from pynput.mouse import Controller as Controller
from pynput.mouse import Button
from pynput import keyboard
from threading import Thread
import mss
import time
import random
import tkinter as tk


# Global variable to track the overlay status
overlay_status = "OFF"
# Screen capture tool instance
sct = mss.mss()

def on_press(key):
    """
    Callback function to be called when a keyboard event occurs.

    Args:
    - key: The key event that was pressed.

    If the key '5' is pressed, it toggles the bot's activity.
    """
    if key == keyboard.KeyCode(char='5'):
        toggle_bot()


def create_overlay():
    """
    Creates an overlay window that displays if the bot is on or off.

    This function creates a transparent top-level window with a label indicating
    the status of the bot, either 'ON' or 'OFF'.
    """
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

    def update_overlay():
        """
        Updates the text of the overlay label to reflect the current status.

        this function schedules itself to be called every 100ms to update the overlay.
        """
        nonlocal label
        label.config(text=overlay_status)
        overlay.after(100, update_overlay)

    # Start the periodic update
    update_overlay()
    # Start the Tkinter event loop
    overlay.mainloop()

def start_overlay():
    """
    Starts the overlay in a separate thread.

    This function allows the main program to run concurrently with the overlay window.
    """
    overlay_thread = Thread(target=create_overlay)
    overlay_thread.daemon = True
    overlay_thread.start()

def toggle_overlay_status(new_status):
    """
    Toggles the overlay status between 'ON' and 'OFF'.

    Args:
    - new_status: The new status to set for the overlay.
    """
    global overlay_status
    overlay_status = new_status

def toggle_bot():
    """
    Toggles the bot activation state.

    This function enables or disables the bot and updates the overlay status accordingly.
    Also handles the mouse button release if the bot is disabled while pressing it.
    """
    global enabled, is_pressed
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
        enabled = True
        toggle_overlay_status("ON")
    time.sleep(0.2)

if __name__ == '__main__':
    print('RUNNING')

    # Initialize the keyboard listener to monitor for start and stop '5' press
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Initialize the mouse controller
    mouse = Controller()

    # Initial state of the bot and mouse press
    enabled = False
    # Variable to track the state of the mouse button
    is_pressed = False

    # Start the overlay to display the bot status
    start_overlay()

    # Define the screen region to capture for detecting changes in this
    # case we have chosen the centre of my 1920x1080 screen, if different screen
    # resolution do (width/2) -1 for left and (height/2) -1 for top
    region = {'top': 539, 'left': 959, 'width': 1, 'height': 1}

    # Main loop to continuously check the screen region and control the mouse
    while True:

        # checks if the bot is active
        if enabled:
            # if the picture value is different the bot will shoot
            img2 = sct.grab(region)
            frame1 = np.array(img2).sum()


            # If frame1 is equal to 638 or 739 press mouse button
            # this is when the reticle is red or orange
            if (frame1 == 638 or frame1 == 739) and not is_pressed:
                # presses mouse after random time between 0.01s-0.05s to simulate human reaction time randomness
                # encase of anticheat heuristics
                number = random.uniform(0.01, 0.05)
                time.sleep(number)
                mouse.press(Button.left)
                is_pressed = True

            # If reticle is not red or orange let go of mouse button
            elif (frame1 != 638 or frame1 != 739) and is_pressed:
                mouse.release(Button.left)
                is_pressed = False

            # Sleep for a short random period if the button is pressed to simulate human clicking speeds
            if is_pressed:
                number = random.uniform(0.1, 0.3)
                time.sleep(number)

