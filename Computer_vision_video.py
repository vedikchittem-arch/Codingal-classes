import cv2
video = cv2.VideoCapture("a.mp4")
if not video.isOpened():
    print("Error video could not be opened")
    exit()

while True:
    ret,frame = video.read()

    if not ret or frame is None:
        print("Frame is empty video cannot be named")
        break
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(gray_frame, (224,224))
    cv2.imshow("Processed image",resized_image)
    key = cv2.waitKey(25) & 0xFF 
    if key == ord('s'):
       cv2.imwrite("grayscale_resized_image.jpeg", resized_image)
       print("Image saved as grayscale_resized_image.jpeg")
video.release()
cv2.destroyAllWindows() 
print(f"processed image dimension {resized_image.shape}")