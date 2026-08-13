import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("family.jpeg")
print(image.shape)

rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
(h, w) = image.shape[:2]
plt.imshow(rgb_image)
plt.show()