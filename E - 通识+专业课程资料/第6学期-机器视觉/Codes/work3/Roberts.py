import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("3-1.jpg")
img_gray = img.convert("L")
img_arr = np.array(img_gray)
h,w = img_arr.shape

img_robert = np.zeros((h,w))

filter_robert_x = np.matrix([[-1,0],[0,1]])
filter_robert_y = np.matrix([[0,-1],[1,0]])
for i in range(1,h-1):
    for j in range(1,w-1):
        img_robert[i,j] = abs(np.sum(np.multiply(img_arr[i-1:i+1,j-1:j+1],filter_robert_x))) + abs(np.sum(np.multiply(img_arr[i-1:i+1,j-1:j+1],filter_robert_y)))

img2 = img_arr - img_robert
img_robert = np.uint8(img_robert)
im2 = np.uint8(img2)

plt.title("roberts")
plt.imshow(img_robert,cmap="gray")
plt.show()

plt.title("img2")
plt.imshow(img2,cmap="gray")
plt.show()
