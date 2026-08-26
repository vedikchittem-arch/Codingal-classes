import cv2

# Load the image
image = cv2.imread("family.jpeg")

# Check if image loaded
if image is None:
    print("Error: Could not find family.jpeg")
    exit()

# Resize the image
small = cv2.resize(image, (200, 200))
medium = cv2.resize(image, (400, 400))
large = cv2.resize(image, (600, 600))

# Display the resized images
cv2.imshow("Small - 200x200", small)
cv2.imshow("Medium - 400x400", medium)
cv2.imshow("Large - 600x600", large)

# Save the resized images
cv2.imwrite("input_image_small.jpg", small)
cv2.imwrite("input_image_medium.jpg", medium)
cv2.imwrite("input_image_large.jpg", large)

print("Images resized and saved successfully!")

# Wait until a key is pressed
cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()