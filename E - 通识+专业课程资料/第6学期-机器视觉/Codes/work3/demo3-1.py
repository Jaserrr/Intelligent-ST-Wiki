import numpy as np
from PIL import Image
import math

img = Image.open("3-1.jpg")
img_gray = img.convert("L")
img_arr = np.array(img_gray)
h,w = img_arr.shape
img_sobel = np.zeros((h,w))

sobel_x = np.matrix([[-1,0,1],[-2,0,2],[-1,0,1]])
sobel_y = np.matrix([[-1,-2,-1],[0,0,0],[1,2,1]])

for i in range(1,h-1):
    for j in range(1,w-1):
        img_sobel[i,j] = math.sqrt((np.sum(np.multiply(img_arr[i-1:i+2,j-1:j+2],sobel_x))) ** 2 + (np.sum(np.multiply(img_arr[i-1:i+2,j-1:j+2],sobel_y))) ** 2)

img1 = np.uint8(img_sobel)
img2 = img_arr + img_sobel
img2 = np.clip(img2,0,255).astype(np.uint8)

Image.fromarray(img1).save("img1.jpg")
Image.fromarray(img2).save("img2.jpg")
