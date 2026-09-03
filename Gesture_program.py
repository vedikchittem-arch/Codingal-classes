import cv2
import mediapipe as mp
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not opened")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# HSV - hue, saturation, value
    lower_skin = np.array([0,20,70], dtype=np.uint8)
    upper_skin = np.array([20,255,255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)