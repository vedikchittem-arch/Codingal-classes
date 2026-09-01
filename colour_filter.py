import cv2
import numpy as np

def apply_filter(image, ftype):
    """Apply a filter to the image based of the filter type"""
    img = image.copy()
    if ftype == "red_tint":
        img[:,:,1] = img[:,:,0] = 0
    elif ftype == "green_tint":
        img[:,:,0] = img[:,:,2] = 0
    elif ftype == "blue_tint":
        img[:,:,1] = img[:,:,2] = 0
    elif ftype == "sobel":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sx = cv2.Sobel(gray, cv2.CV_64F, 1,0, ksize= 3)
        sy = cv2.Sobel(gray, cv2.CV_64F, 1,0, ksize= 3)
        sob = cv2.bitwise_or(sx.astype("Uint8").sy.astype("Uint8"))
        img = cv2.cvtColor(sob, cv2.COLOR_GRAY2BGR)
    elif ftype == "canny":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(gray,100,200)
        img = cv2.cvtColor(can, cv2.COLOR_GRAY2BGR)
    elif ftype == "cartoon":
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(image, 9, 300, 300)
        img = cv2.bitwise_and(color, color, mask=edges)
    return img

def main():
    cap = 