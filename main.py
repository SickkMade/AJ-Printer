from PIL import Image
import pyautogui
import time
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
        image = Image.open("your_image.png").convert("RGB").quantize(colors=12).convert('RGB') #caps at 12 colors
    except FileNotFoundError:
        print("Image file not found.")
        return

    color_coordinates = {}
    unique_colors = set(image.getdata())
    visited = set()

    dominant_color = Counter(image.getdata()).most_common(1)[0][0]
    change_color(dominant_color)
    fill_bucket(width_min,0)

    unique_colors.remove(dominant_color) #i set background to most used color! then remove it from a color i need to draw

    # Get all unique colors in the image and their coordinates
    for y in range(0, height_max - height_min + 1): #loop through in dict create each color element that lists it's x, y pos\
        #last_color = None
        for x in range(0, width_max - width_min):
            pixel_color = image.getpixel((x, y)) #current pixle color
            if((x,y) not in visited): #if weve never checked here before
                if pixel_color not in color_coordinates:
                    color_coordinates[pixel_color] = []
                color_coordinates[pixel_color].append([])
                for x1, y1 in find_outline(x,  y, image, pixel_color, visited): #a whole flooded area
                    color_coordinates[pixel_color][-1].append((x1, y1))
                
    for pixel_color in unique_colors:
        change_color(pixel_color)
        for arr in color_coordinates[pixel_color]:
            click(arr)


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

def click(arr): #given an array with an unknown shape outline and fill it in
    if len(arr) <= 0:
        return
    
    # Move the mouse to the starting position
    
    pyautogui.moveTo(arr[0][0] + width_min, arr[0][1])
    pyautogui.mouseDown()
    time.sleep(0.2)
    # Press the mouse button to start dragging
    

    # Move the mouse to each subsequent point in the outline
    for x, y in arr[1:]:
        pyautogui.moveTo(x + width_min, y, duration=0)
        time.sleep(0.05)
    # Release the mouse button to finish dragging
    pyautogui.mouseUp()
    time.sleep(0.1)

def find_outline(x, y, image, pixel_color, visited):
    outline = set()
    stack = [(x, y)]


    while stack:
        x, y = stack.pop()

        # Check all neighboring pixels
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy

            # Ensure the neighboring pixel is within bounds
            if 0 <= nx < width_max - width_min and 0 <= ny < height_max - height_min:
                # If the neighboring pixel is not the same color, it's part of the outline
                if image.getpixel((nx, ny)) != pixel_color:
                    outline.add((nx, ny))
                # If it's the same color and hasn't been visited yet, add it to the stack
                elif (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append((nx, ny))

    return outline


main()



#way to fing slow
