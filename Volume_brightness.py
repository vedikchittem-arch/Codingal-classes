
import cv2
import numpy as np

# Error handling for required libraries
try:
    import mediapipe as mp
    import screen_brightness_control as sbc
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from comtypes import CLSCTX_ALL
except ImportError as e:
    print("Missing library:", e)
    print("Run: pip install opencv-python mediapipe numpy pycaw comtypes screen-brightness-control")
    raise SystemExit

# Windows volume setup
try:
    device = AudioUtilities.GetSpeakers()
    volume = device.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
    ).QueryInterface(IAudioEndpointVolume)
    vmin, vmax, _ = volume.GetVolumeRange()
except Exception as e:
    print("Volume setup error:", e)
    volume = None

# Brightness setup
try:
    sbc.list_monitors()
    brightness_ok = True
except Exception as e:
    print("Brightness setup error:", e)
    brightness_ok = False

# Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("ERROR: Webcam could not open.")
    raise SystemExit

# Settings
MIN_DIST, MAX_DIST = 30, 220
smooth = [50.0, 50.0]
last_brightness = -1
frame_count = 0

def bar(img, x, y, value, name):
    value = int(np.clip(value, 0, 100))
    cv2.rectangle(img, (x, y), (x+35, y+200), (60,60,60), -1)
    cv2.rectangle(img, (x, y+200-int(value*2)),
                  (x+35, y+200), (0,200,0), -1)
    cv2.rectangle(img, (x, y), (x+35, y+200), (255,255,255), 2)
    cv2.putText(img, f"{name}: {value}%", (x-10, y+230),
                cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)

try:
    while True:
        ok, img = cap.read()
        if not ok:
            print("Webcam frame failed.")
            break

        img = cv2.flip(img, 1)
        h, w = img.shape[:2]
        result = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        frame_count += 1

        if result.multi_hand_landmarks:
            for hand, handed in zip(
                result.multi_hand_landmarks,
                result.multi_handedness
            ):
                # Thumb and index fingertips
                a = hand.landmark[4]
                b = hand.landmark[8]
                p1 = (int(a.x*w), int(a.y*h))
                p2 = (int(b.x*w), int(b.y*h))

                dist = np.linalg.norm(np.array(p1)-np.array(p2))
                value = int(np.interp(dist, [MIN_DIST, MAX_DIST], [0,100]))
                label = handed.classification[0].label

                # Draw hand and distance
                mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)
                cv2.line(img, p1, p2, (255,0,255), 3)
                cv2.circle(img, p1, 7, (0,255,0), -1)
                cv2.circle(img, p2, 7, (0,255,0), -1)

                # Left hand = volume, right hand = brightness
                if label == "Left":
                    smooth[0] = .75*smooth[0] + .25*value
                    if volume:
                        level = np.interp(smooth[0], [0,100], [vmin,vmax])
                        try:
                            volume.SetMasterVolumeLevel(float(level), None)
                        except Exception:
                            pass
                else:
                    smooth[1] = .75*smooth[1] + .25*value
                    if brightness_ok and frame_count % 3 == 0:
                        try:
                            new_brightness = int(smooth[1])
                            if abs(new_brightness-last_brightness) >= 2:
                                sbc.set_brightness(new_brightness)
                                last_brightness = new_brightness
                        except Exception:
                            pass

        # Visual feedback
        bar(img, 40, 100, smooth[0], "VOL")
        bar(img, 120, 100, smooth[1], "BRI")

        cv2.putText(img, "Q: Quit | S: Swap hands (manual code change)",
                    (200, 40), cv2.FONT_HERSHEY_SIMPLEX, .55, (255,255,255), 2)
        cv2.imshow("Hand Control", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    print("Program closed.")