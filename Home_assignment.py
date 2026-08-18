#make the photo ready for a party
#imagine your image is going to win a photo party you have to perform two operations 
#task 
#task 1 is to read an image using opencv
#rotate the image by 90 degrees
#increase its brightness by thirty
#display the final image with the title party ready image

import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("family.jpeg")
print(image.shape)

rgb_image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
(h , w ) = image.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center,90,1.0)
rotated = cv2.warpAffine(image,M,(w,h))
rotated_rgb = cv2.cvtColor(rotated,cv2.COLOR_BGR2RGB)
plt.imshow(rotated_rgb)
plt.show()
# increase brightness
brightness_metrix = np.ones(image.shape, dtype = "uint 8") * 30
# add brightness
brighter = cv2.add(image,brightness_metrix)
brighter_rgb = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
plt.title("Party ready image", )
plt.imshow(brighter_rgb)
plt.show()