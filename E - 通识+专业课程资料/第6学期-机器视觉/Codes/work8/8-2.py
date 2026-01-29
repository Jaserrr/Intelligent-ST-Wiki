import cv2
import numpy as np

img = cv2.imread('Snoopy-small.jpg')
h,w,c = img.shape
new_h,new_w = h*10, w*10

res_nearest = np.zeros((new_h, new_w, c), dtype=img.dtype)
for i in range(new_h):
    for j in range(new_w):
        res_nearest[i,j] = img[i//10, j//10]

cv2.imwrite('nearest.jpg', res_nearest)