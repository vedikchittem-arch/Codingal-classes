import cv2, time, pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)
mp_drawing = mp.solutions.drawing_utils

#configurations
SCROLL_SPEED = 300
SCROLL_DELAY = 1
CAM_WIDTH, CAM_HEIGHT = 640, 480

def 