import cv2
import numpy as np
import tensorflow as tf

import tensorflow as tf

model = tf.keras.models.load_model(
    "emotion_model_final_nb.keras",
    compile=False
)

print("Model loaded successfully!")

emotions = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

# Face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

print("Camera opened successfully:", cap.isOpened())

if not cap.isOpened():
    print("Error: Could not open the camera")
    exit()

while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        # FER2013 uses 48x48 images
        face = cv2.resize(face, (48, 48))

        # Normalize
        face = face.astype("float32") / 255.0

        # Prepare for model
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)

        # Predict
        prediction = model.predict(face, verbose=0)

        emotion_index = np.argmax(prediction)
        emotion = emotions[emotion_index]

        confidence = prediction[0][emotion_index] * 100

        # Draw face
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Display emotion
        cv2.putText(
            frame,
            f"{emotion} {confidence:.1f}%",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    cv2.imshow("FER2013 Emotion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()