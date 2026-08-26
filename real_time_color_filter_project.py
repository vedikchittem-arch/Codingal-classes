import cv2
import numpy as np
import os
import re

# Load image
image = cv2.imread("family.jpeg")

if image is None:
    print("Error: Could not load image.")
    exit()

# Make a copy to work with
output = image.copy()

# Channel intensities
red = 0
green = 0
blue = 0

while True:

    # Start with original image
    output = image.copy()

    # Apply channel changes
    output[:, :, 2] = np.clip(output[:, :, 2].astype(int) + red, 0, 255)
    output[:, :, 1] = np.clip(output[:, :, 1].astype(int) + green, 0, 255)
    output[:, :, 0] = np.clip(output[:, :, 0].astype(int) + blue, 0, 255)

    # Show image
    cv2.imshow("Interactive Image Filter", output)

    key = cv2.waitKeyEx(0)

    # Red tint
    if key == ord('r'):
        red += 50

    # Green tint
    elif key == ord('g'):
        green += 50

    # Blue tint
    elif key == ord('b'):
        blue += 50

    # Increase red
    elif key == ord('i'):
        red += 25

    # Decrease blue
    elif key == ord('d'):
        blue -= 25

    # Increase green
    elif key == 2490368:       # Up arrow I learned from searching online
        green += 25

    # Decrease red
    elif key == 2621440:       # Down arrow i learned from searching online
        red -= 25

    # Quit
    elif key == ord('q'):
        # Ask whether to save
        answer = input("Do you want to save the image? (y/n): ")

        if answer.lower() == 'y':
            filename = input("Enter a filename: ")

            if filename == "":
                filename = "edited_image"


            save_path = os.path.join("images", filename)

            cv2.imwrite(save_path, output)

            print("Image saved as:", save_path)
    else:
        print("Invalid key! Please use r, g, b, i, d, up arrow, down arrow, or q to quit.")

        break

cv2.destroyAllWindows()