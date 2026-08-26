import cv2

image = cv2.imread("family.jpeg")


h, w = image.shape[:2]


image = cv2.resize(image, (w, h // 2))

h, w = image.shape[:2]
y = h // 2

cv2.arrowedLine(image, (10, y), (w - 10, y), (0, 255, 0), 3)
cv2.arrowedLine(image, (w - 10, y), (10, y), (0, 255, 0), 3)

cv2.putText(image, f"Width: {w}px", (w // 2 - 80, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imwrite("output_images/width.jpg", image)

cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

