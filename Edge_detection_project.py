import cv2

# Load image
image = cv2.imread("family.jpeg")

if image is None:
    print("Image not found!")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

while True:
    print("\n--- Image Processing Program ---")
    print("1. Gaussian Blur")
    print("2. Median Blur")
    print("3. Sobel Edge Detection")
    print("4. Canny Edge Detection")
    print("5. Laplacian Edge Detection")
    print("6. Show Original Image")
    print("7. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        processed = cv2.GaussianBlur(image, (5, 5), 0)
        cv2.imshow("Original", image)
        cv2.imshow("Gaussian Blur", processed)

    elif choice == "2":
        processed = cv2.medianBlur(image, 5)
        cv2.imshow("Original", image)
        cv2.imshow("Median Blur", processed)

    elif choice == "3":
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

        processed = cv2.magnitude(sobel_x, sobel_y)
        processed = cv2.convertScaleAbs(processed)

        cv2.imshow("Original", image)
        cv2.imshow("Sobel", processed)

    elif choice == "4":
        processed = cv2.Canny(gray, 100, 200)

        cv2.imshow("Original", image)
        cv2.imshow("Canny", processed)

    elif choice == "5":
        processed = cv2.Laplacian(gray, cv2.CV_64F)
        processed = cv2.convertScaleAbs(processed)

        cv2.imshow("Original", image)
        cv2.imshow("Laplacian", processed)

    elif choice == "6":
        cv2.imshow("Original", image)

    elif choice == "7":
        break

    else:
        print("Invalid choice!")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

cv2.destroyAllWindows()