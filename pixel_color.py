# USED TO FIND THE DIFFERENT RETICLE PIXEL COLOURS
from PIL import Image

with Image.open('pixel_off.png') as img:
    x = 1
    y = 1
    color = img.getpixel((x, y))
    print(color)