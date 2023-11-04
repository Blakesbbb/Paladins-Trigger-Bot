#THIS IS USED TO FIGURE OUT WHAT WAS BOTTLE NECKING
#THE TRIGGER BOT AND MAKING IT RUN TOO SLOW TO WORK REALISTICALLY


import cProfile
import pstats
import numpy as np
import keyboard
from pynput.mouse import Controller as Controller
from pynput.mouse import Button
import time
import random
import tkinter as tk
from threading import Thread
import mss
from pynput import keyboard
overlay_status = "OFF"
sct = mss.mss()
def main():



    def create_overlay():
        global overlay_status
        overlay = tk.Tk()
        overlay.title("Trigger Bot")

        overlay.geometry("100x50+10+10")

        overlay.attributes("-transparentcolor", "white")

        label = tk.Label(overlay, text=overlay_status, bg="white", font=("Helvetica", 20))
        label.pack(expand=True, fill="both")

        overlay.overrideredirect(True)

        overlay.attributes("-topmost", True)

        def update_overlay():
            nonlocal label
            label.config(text=overlay_status)
            overlay.after(1000, update_overlay)

        update_overlay()
        overlay.mainloop()

    def start_overlay():
        overlay_thread = Thread(target=create_overlay)
        overlay_thread.daemon = True
        overlay_thread.start()

    def toggle_overlay_status(new_status):
        global overlay_status
        overlay_status = new_status

    mouse = Controller()
    enabled = False
    is_pressed = False
    start_overlay()
    region = {'top': 539, 'left': 959, 'width': 1, 'height': 1}

    for _ in range(100):

        if keyboard.is_pressed('5'):
            if enabled:
                print("Disabled")
                toggle_overlay_status("OFF")
                enabled = False
                if is_pressed:
                    mouse.release(Button.left)
                    is_pressed = False
            else:
                print("Enabled")
                enabled = True
                toggle_overlay_status("ON")

            time.sleep(0.2)


        if enabled:

            img2 = sct.grab(region)
            frame1 = np.array(img2).sum()
            print(frame1)

            if (frame1 == 638 or frame1 == 739) and not is_pressed:
                number = random.uniform(0.01, 0.05)
                time.sleep(number)
                mouse.press(Button.left)
                is_pressed = True


            elif (frame1 != 638 and frame1 != 739) and is_pressed:
                mouse.release(Button.left)
                is_pressed = False


            if is_pressed:
                number = random.uniform(0.1, 0.3)
                time.sleep(number)



    pass
if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()