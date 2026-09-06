import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open camera.")
    exit()

mode = "NORMAL"

print("""
Camera Controls
---------------
R = Red Mode 🍎
G = Green Alien Mode 👽
C = Canny X-Ray Mode 🩻
T = Cartoon Mode 📺
Q = Quit 🚪
""")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame.")
        break


    if mode == "RED":
        blue, green, red = cv2.split(frame)

        zero = np.zeros_like(blue)

        frame = cv2.merge([
            zero,
            zero,
            red
        ])

   
    elif mode == "GREEN":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.merge([
            np.zeros_like(gray),
            gray,
            np.zeros_like(gray)
        ])

   
    elif mode == "CANNY":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur( gray,(5, 5),0)

        edges = cv2.Canny(blur,50,150)

        
        frame = cv2.bitwise_not(edges)

        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)

   
    elif mode == "CARTOON":

        # Smooth colours
        smooth = cv2.bilateralFilter(
            frame,
            9,
            75,
            75
        )

        # Find outlines
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.medianBlur(
            gray,
            7
        )

        edges = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            9,
            9
        )

        edges = cv2.cvtColor(
            edges,
            cv2.COLOR_GRAY2BGR
        )

        frame = cv2.bitwise_and(
            smooth,
            edges
        )

    # Show current mode
    cv2.putText(
        frame,
        f"MODE: {mode}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )
    cv2.imshow(
        "Fun OpenCV Camera",
        frame
    )
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        mode = "RED"
        print("🍎 Red Mode")

    elif key == ord("g"):
        mode = "GREEN"
        print("👽 Green Alien Mode")

    elif key == ord("c"):
        mode = "CANNY"
        print("🩻 Canny X-Ray Mode")

    elif key == ord("t"):
        mode = "CARTOON"
        print("📺 Cartoon Mode")

    elif key == ord("q"):
        print("🚪 Goodbye!")
        break

cap.release()
cv2.destroyAllWindows()  