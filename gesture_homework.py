
import cv2
import mediapipe as mp
import numpy as np

# Error handling
try:
    hands = mp.solutions.hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
except Exception as e:
    print("Hand tracking error:", e)
    raise SystemExit

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Webcam failed to open.")
    raise SystemExit

# Shape settings
x, y = 400, 300
size = 50
colour = (0, 255, 0)
previous = None
movement = "Not detected"

try:
    while True:
        ok, frame = cap.read()

        if not ok:
            print("ERROR: Could not capture frame.")
            break

        frame = cv2.flip(frame, 1)
        h, w = frame.shape[:2]
        result = hands.process(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

        movement = "Not detected"

        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            p = hand.landmark[8]  # Index fingertip
            wrist = hand.landmark[0]
            middle = hand.landmark[12]

            # Finger position
            px, py = int(p.x*w), int(p.y*h)

            # Movement detection
            if previous:
                dx, dy = px-previous[0], py-previous[1]

                if abs(dx) > abs(dy) and abs(dx) > 8:
                    movement = "Right" if dx > 0 else "Left"
                    x = np.clip(x + dx, 30, w-30)

                elif abs(dy) > 8:
                    movement = "Down" if dy > 0 else "Up"
                    y = np.clip(y + dy, 30, h-30)

            previous = (px, py)

            # Dynamic size based on hand distance
            distance = abs(
                middle.y - wrist.y
            )
            size = int(np.clip(distance*250, 25, 120))

            # Detect thumbs-up
            thumb = hand.landmark[4]
            index = hand.landmark[8]
            thumb_up = (
                thumb.y < wrist.y and
                index.y > thumb.y
            )

            if thumb_up:
                colour = (0, 0, 255)  # Red
            else:
                colour = (0, 255, 0)  # Green

            # Draw hand landmarks
            mp.solutions.drawing_utils.draw_landmarks(
                frame, hand, mp.solutions.hands.HAND_CONNECTIONS
            )

        else:
            previous = None

        # Draw shape
        cv2.circle(
            frame, (int(x), int(y)), size, colour, -1
        )

        # Feedback
        cv2.putText(
            frame, "Movement: " + movement, (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, .8, (255,255,255), 2
        )

        cv2.putText(
            frame, "Thumbs up = Red | Normal = Green",
            (20, 75), cv2.FONT_HERSHEY_SIMPLEX, .6,
            (255,255,255), 2
        )

        cv2.putText(
            frame, "Q = Quit", (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX, .6,
            (255,255,255), 2
        )

        cv2.imshow("Hand Gesture Project", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Program closed.")