import cv2
import time
import math
import pyautogui
import mediapipe as mp

# MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Settings
SCROLL_SPEED = 300
SCROLL_DELAY = 0.15
CAM_WIDTH, CAM_HEIGHT = 640, 480

def detect_gesture(hand, handedness):
    fingers = []

    # Index, middle, ring and pinky
    tips = [
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    for tip in tips:
        if hand.landmark[tip].y < hand.landmark[tip - 2].y:
            fingers.append(1)

    # Thumb
    thumb = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = hand.landmark[mp_hands.HandLandmark.THUMB_IP]

    if (handedness == "Right" and thumb.x > thumb_ip.x) or \
       (handedness == "Left" and thumb.x < thumb_ip.x):
        fingers.append(1)

    if len(fingers) == 5:
        return "OPEN PALM"
    elif len(fingers) == 0:
        return "FIST"
    else:
        return "NONE"


cap = cv2.VideoCapture(0)
cap.set(3, CAM_WIDTH)
cap.set(4, CAM_HEIGHT)

last_scroll = 0
previous_time = time.time()

print("Gesture Scroll Control")
print("Open palm = Scroll Up")
print("Fist = Scroll Down")
print("Press Q to quit")

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "NONE"
    handedness = "Unknown"
    scroll_amount = 0

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        if results.multi_handedness:
            handedness = results.multi_handedness[0].classification[0].label

        gesture = detect_gesture(hand, handedness)

        # Get thumb and index positions
        thumb = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Distance between thumb and index
        distance = math.sqrt(
            (thumb.x - index.x) ** 2 +
            (thumb.y - index.y) ** 2
        )

        # Convert distance into scrolling speed
        speed = int(
            min(max(distance * SCROLL_SPEED * 10, 50), SCROLL_SPEED)
        )

        scroll_amount = speed

        # Scroll after the delay
        if time.time() - last_scroll > SCROLL_DELAY:

            if gesture == "OPEN PALM":
                pyautogui.scroll(scroll_amount)
                last_scroll = time.time()

            elif gesture == "FIST":
                pyautogui.scroll(-scroll_amount)
                last_scroll = time.time()

        # Draw hand
        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Show thumb-index distance
        cv2.putText(
            frame,
            f"Distance: {distance:.2f}",
            (10, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Speed: {speed}",
            (10, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    # Feedback
    cv2.putText(frame,f"FPS: {int(fps)}",(10, 30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 0, 0),2)

    cv2.putText(frame,f"Hand: {handedness}",(350, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(255, 0, 0), 2)

    cv2.putText(frame,f"Gesture: {gesture}",(350, 60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255, 0, 0),2)

    cv2.imshow("Gesture Scroll Control", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()