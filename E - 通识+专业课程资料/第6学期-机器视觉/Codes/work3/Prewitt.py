import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math

img = Image.open("3-1.jpg")
img_gray = img.convert("L")
img_arr = np.array(img_gray)
h,w = img_arr.shape

img_prewitt = np.zeros((h,w))

filter_prewitt_x = np.matrix([[-1,0,1],[-1,0,1],[-1,0,1]])
filter_prewitt_y = np.matrix([[-1,-1,-1],[0,0,0],[1,1,1]])

for i in range(1,h-1):
    for j in range(1,w-1):
        img_prewitt[i,j] = math.sqrt((np.sum(np.multiply(img_arr[i-1:i+2,j-1:j+2],filter_prewitt_x))) ** 2 + (np.sum(np.multiply(img_arr[i-1:i+2,j-1:j+2],filter_prewitt_y))) ** 2)

img_prewitt = np.uint8(img_prewitt)
img2 = np.uint8(img_arr - img_prewitt)

plt.title("prewitt")
plt.imshow(img_prewitt,cmap="gray")
plt.show()

plt.title("img2")
plt.imshow(img2,cmap="gray")
plt.show()