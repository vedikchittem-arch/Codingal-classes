#Create a program that opens the webcam and shows a funny message based on the number of detected faces
# for zero face where is everybody
# one face say hey boss 😎
# two faces say Party has started 🥳🥳🎉
# 

import cv2

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
cv2.destroyAllWindows()

# create a python opencv camera program that 
# R = red mode 🍎
# G = green alien mode 👽
# C = canny xray mode 🩻
# T = Cartoon mode 📺
# Q = quit 🚪

