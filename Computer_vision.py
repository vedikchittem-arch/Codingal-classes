import cv2
image = cv2.imread("C:\\Users\\Vedik\\Pictures\\Family pictures\\a.jpeg")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
resized_image = cv2.resize(gray, (224,224))
cv2.imshow("Processed image",resized_image)
key = cv2.waitKey(0) 
if key == ord('s'):
    cv2.imwrite("grayscale_resized_image.jpeg", resized_image)
    print("Image saved as grayscale_resized_image.jpeg")
else:
    print("Image not saved")
cv2.destroyAllWindows() 
print(f"processed image dimension {resized_image.shape}")