import cv2
print(cv2.__file__)
print(cv2.__version__)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascades_frontalface_default.xml")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open the camera")
    exit

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 
                                          scaleFactor = 1.1,
                                          minNeighbors = 5,
                                          minSize = (30, 30)  
                                          )

    