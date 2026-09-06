import cv2
import numpy as np


def apply_filter(image, filter_type):
    """Apply the selected filter to the image."""

    img = image.copy()

    # Red tint
    if filter_type == "red":
        img[:, :, 0] = 0   # Remove blue
        img[:, :, 1] = 0   # Remove green

    # Green tint
    elif filter_type == "green":
        img[:, :, 0] = 0   # Remove blue
        img[:, :, 2] = 0   # Remove red

    # Blue tint
    elif filter_type == "blue":
        img[:, :, 1] = 0   # Remove green
        img[:, :, 2] = 0   # Remove red

    # Sobel edge detection
    elif filter_type == "sobel":

        gray = cv2.cvtColor( image,cv2.COLOR_BGR2GRAY)

        sobel_x = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)
        sobel_y = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)

        sobel_x = cv2.convertScaleAbs(sobel_x)
        sobel_y = cv2.convertScaleAbs(sobel_y)

        sobel = cv2.bitwise_or(sobel_x,sobel_y)

        img = cv2.cvtColor(
            sobel,
            cv2.COLOR_GRAY2BGR
        )

    # Canny edge detection
    elif filter_type == "canny":

        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray,100,200)
        img = cv2.cvtColor(edges,cv2.COLOR_GRAY2BGR)

    return img


image_path = "family.jpeg"

image = cv2.imread(image_path)

if image is None:
    print("Error: Could not load image.")
    print("Check that the image path is correct.")
    exit()


# Start with normal image
current_filter = "normal"


print("Image Filter Program")
print("--------------------")
print("R = Red")
print("G = Green")
print("B = Blue")
print("S = Sobel")
print("C = Canny")
print("N = Normal")
print("Q = Quit")


while True:

    # Apply selected filter to original image
    filtered_image = apply_filter(image,current_filter)

    # Display image
    cv2.imshow("Image Filters",filtered_image)

    # Wait for keyboard input
    key = cv2.waitKey(0) & 0xFF

    if key == ord("r"):
        current_filter = "red"
        print("Red filter selected")

    elif key == ord("g"):
        current_filter = "green"
        print("Green filter selected")

    elif key == ord("b"):
        current_filter = "blue"
        print("Blue filter selected")

    elif key == ord("s"):
        current_filter = "sobel"
        print("Sobel edge detection selected")

    elif key == ord("c"):
        current_filter = "canny"
        print("Canny edge detection selected")

    elif key == ord("n"):
        current_filter = "normal"
        print("Normal image selected")

    elif key == ord("q"):
        print("Closing program...")
        break

    else:
        print(
            "Invalid key. Use R, G, B, S, C, N or Q."
        )


cv2.destroyAllWindows()