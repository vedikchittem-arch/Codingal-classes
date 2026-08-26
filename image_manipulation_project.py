import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread("family.jpeg")

if image is None:
    print("Image could not be found!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Crop the image
cropped = image[100:300, 200:400]

# Rotate the image by 45 degrees
height, width = image.shape[:2]
centre = (width // 2, height // 2)

rotation_matrix = cv2.getRotationMatrix2D(centre, 45, 1)
rotated = cv2.warpAffine(image, rotation_matrix, (width, height))

# Increase brightness
brightness_matrix = np.ones(image.shape, dtype="uint8") * 50
brightened = cv2.add(image, brightness_matrix)

# Save all images
cv2.imwrite("family.jpg", gray)
cv2.imwrite("family.jpg", cropped)
cv2.imwrite("family.jpg", rotated)
cv2.imwrite("family.jpg", brightened)

# Display all results
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))
plt.title("Cropped Image")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB))
plt.title("Rotated Image - 45 Degrees")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(brightened, cv2.COLOR_BGR2RGB))
plt.title("Brightened Image")
plt.axis("off")

plt.tight_layout()
plt.show()

print("All images have been processed and saved!")

# first step was to read the image using opencv,
# then we converted the image to grayscale, cropped it, rotated it by 45 degrees, and increased its brightness. 
# Finally, we saved all the processed images and displayed them using matplotlib.