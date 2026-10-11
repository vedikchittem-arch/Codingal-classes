
import cv2, mediapipe as mp, numpy as np, time

hands = mp.solutions.hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)
filter = 0
last = 0
message = ""
filters = ["Original", "Grayscale", "Sepia", "Negative", "Blur"]

while cam.isOpened():
    ok, frame = cam.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        draw.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
        p = hand.landmark
        h, w = frame.shape[:2]

        
        def dist(a, b):
            return np.hypot((p[a].x-p[b].x)*w, (p[a].y-p[b].y)*h)

        now = time.time()
        if now-last > 1:
            if dist(4, 8) < 35:            
                name = f"photo_{int(now)}.jpg"
                cv2.imwrite(name, frame)
                message = "Photo saved: " + name
                last = now
            elif dist(4, 12) < 35:         
                filter = 1
                message, last = "Grayscale selected", now
            elif dist(4, 16) < 35:         
                filter = 2
                message, last = "Sepia selected", now
            elif dist(4, 20) < 35:         
                filter = 3
                message, last = "Negative selected", now
            elif dist(4, 0) < 35:          
                filter = 4
                message, last = "Blur selected", now

   
    if filter == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    elif filter == 2:
        kernel = np.array([[.272,.534,.131],[.349,.686,.168],[.393,.769,.189]])
        frame = cv2.transform(frame, kernel).clip(0, 255).astype(np.uint8)
    elif filter == 3:
        frame = 255-frame
    elif filter == 4:
        frame = cv2.GaussianBlur(frame, (25, 25), 0)

    cv2.putText(frame, "Filter: "+filters[filter], (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, .7, (0,255,0), 2)
    cv2.putText(frame, message, (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (0,255,255), 1)
    cv2.imshow("Gesture Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
