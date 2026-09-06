#Create a program that opens the webcam and shows a funny message based on the number of detected faces
# for zero face where is everybody
# one face say hey boss 😎
# two faces say Party has started 🥳🥳🎉
# 

"""import cv2

from PIL import Image, ImageDraw, ImageFont

# Open webcam
cap = cv2.VideoCapture(0)

# Load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
font_path = "C:/Windows/Fonts/seguiemj.ttf"
font = ImageFont.truetype(font_path, 32)

while True:
    ret, frame = cap.read()

    if not ret:
        break
    pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Number of faces
    face_count = len(faces)

    # Choose message
    if face_count == 0:
        message = "Where is everybody?"
    elif face_count == 1:
        message = "Hey boss 😎"
    elif face_count == 2:
        message = "Party has started 🥳🥳🎉"
    else:
        message = f"Wow! {face_count} people here! 🎉"

    # Display message
    draw.text((20, 20), message, font= font, fill= (255, 255, 0))
    frame = cv2.cvtColor(pil_image, cv2.COLOR_RGB2BGR)

    
    cv2.imshow("Funny Face Detector", frame)

    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Close everything
cap.release()
cv2.destroyAllWindows()"""

# create a python opencv camera program that 
# R = red mode 🍎
# G = green alien mode 👽
# C = canny xray mode 🩻
# T = Cartoon mode 📺
# Q = quit 🚪

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


