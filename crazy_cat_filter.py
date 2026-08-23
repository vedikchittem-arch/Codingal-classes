"""A cat picture is loaded into the program. The user can press different keys to give the cat funny
colour and effects.
For example: r -> red, b -> blue, g -> green, i -> increase red, d -> decrease blue, o -> original, q-> quit
create a function for apply_cat_filter"""

import cv2
import numpy as np

def apply_colour_filter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == "red_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,0] = 0
    elif filter_type == "blue_tint":
        filtered_image[:,:,1] = 0
        filtered_image[:,:,2] = 0
    elif filter_type == "green_tint":
        filtered_image[:,:,0] = 0
        filtered_image[:,:,2] = 0
    elif filter_type == "increase_red":
        filtered_image[:,:,2] = cv2.add(filtered_image[:,:,2],50)
    elif filter_type == "decrease_blue":
        filtered_image[:,:,0] = cv2.subtract(filtered_image[:,:,0],50)
    elif filter_type == "original":
        filtered_image = image.copy()
    return filtered_image

image_path = "Cat.jpg"

image = cv2.imread(image_path)
if image is None:
    print("Image is not present")
else:
    filter_type = "original"
    print("Press the following keys to apply filters: ")
    print("r-red tint")
    print("b-blue tint")
    print("g-green tint")
    print("i-increase red intensity")
    print("d-decrease blue intensity")
    print("o-original")
    print("q-quit")

    while True:
        filter_image = apply_colour_filter(image,filter_type)
        display_image = cv2.resize(filter_image, (400, 200))
        cv2.imshow("filter_image",display_image)
        key = cv2.waitKey(0) & 0xFF

        if key == ord('r'):
            filter_type = "red_tint"
        elif key == ord('b'):
            filter_type = "blue_tint"
        elif key == ord('g'):
            filter_type = "green_tint"
        elif key == ord('i'):
            filter_type = "increase_red"
        elif key == ord('d'):
            filter_type = "decrease_blue"
        elif key == ord('o'):
            filter_type = "original"
        elif key == ord('q'):
            print("exiting ...")
            break
        else:
            print("Invalid key! Please use r,b,g,i,d,o,q")
    cv2.destroyAllWindows()
        


