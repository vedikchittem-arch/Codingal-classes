import cv2
import mediapipe as mp, numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

Hands = mp.solutions.hands
#creating the hand detector
hands = Hands.Hands(min_detection_confidence = 0.7, min_tracking_confidence = 0.7)

#drawing utility
draw = mp.solutions.drawing_utils

#selecting thumb and index finger
TH,IX = Hands.HandLandmark.THUMB_TIP,
Hands.HandLandmark.INDEX_FINGER_TIP