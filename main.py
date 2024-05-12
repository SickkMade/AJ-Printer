from PIL import Image
import pyautogui
import time
import math
from collections import Counter

width_min = 358
width_max = 1678
height_min = 0
height_max = 1079
def main():
    pyautogui.PAUSE = .01
    # Wait for 3 seconds before starting
    time.sleep(3)

    # Load the image
    try:
        image = Image.open("your_image.jpg").convert("RGB").quantize(colors=3).convert('RGB') #caps at 12 colors
    except FileNotFoundError:
        print("Image file not found.")
        return

    color_coordinates = {}
    unique_colors = set(image.getdata())


    dominant_color = Counter(image.getdata()).most_common(1)[0][0]
    change_color(dominant_color)
    fill_bucket(width_min,0)

    unique_colors.remove(dominant_color) #i set background to most used color! then remove it from a color i need to draw


    # Get all unique colors in the image and their coordinates
    for y in range(0, height_max - height_min + 1): #loop through in dict create each color element that lists it's x, y pos\
        last_color = None
        for x in range(0, width_max - width_min):
            pixel_color = image.getpixel((x, y))
            if pixel_color == last_color:
                # Continue the streak of the same color
                color_coordinates[pixel_color][-1].append((x + width_min, y))
            else:
                # New color or non-adjacent pixels
                if pixel_color not in color_coordinates:
                    color_coordinates[pixel_color] = []
                color_coordinates[pixel_color].append([(x + width_min, y)])

            last_color = pixel_color
                
    for pixel_color in unique_colors:
        change_color(pixel_color)
        for arr in color_coordinates[pixel_color]:
            click(arr)


def fill_bucket(x, y): #use fillbucket at given location then switch back to paint tool
    pyautogui.click(50, 365)
    time.sleep(.3)
    pyautogui.click(230, 210)
    time.sleep(.3)
    pyautogui.click(865, 75)
    time.sleep(.1)
    pyautogui.click(x,y)
    time.sleep(5)

    pyautogui.click(50, 365)
    time.sleep(.1)
    pyautogui.click(765, 210)
    time.sleep(.3)
    pyautogui.click(865, 75)

def change_color(hex_code):
    # Click the color button
    pyautogui.click(50, 50)
    time.sleep(.1)

    # Click the color text hex box
    pyautogui.click(1000, 1000)
    time.sleep(.1)
    # Type the color hex code
    pyautogui.write('#%02x%02x%02x' % hex_code, interval=0)
    time.sleep(.1)
    # Press Enter to apply the color
    pyautogui.press('enter')
    time.sleep(.1)
    # Click the X to close the color picker
    pyautogui.click(1400, 60)
    time.sleep(.1)

def click(arr): #arr is arr of x, y in a row horizontally
    pyautogui.moveTo(arr[0])
    pyautogui.mouseDown()
    pyautogui.moveTo(*arr[-1], .2)
    time.sleep(0.05)
    pyautogui.mouseUp()
    time.sleep(0.05)
    





def rgb_distance(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return math.sqrt((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)

def are_colors_close(color1, color2, threshold=25):
    distance = rgb_distance(color1, color2)
    return distance <= threshold











main()



#way to fing slow
