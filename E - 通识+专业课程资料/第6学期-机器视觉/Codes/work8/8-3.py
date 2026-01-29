import cv2
import numpy as np

img = cv2.imread('Snoopy-small.jpg')
h,w,c = img.shape
new_h,new_w = h*10, w*10
res_linear = np.zeros((new_h, new_w, c), dtype=np.uint8)

for i in range(new_h):
    for j in range(new_w):
        # 映射回原图坐标（浮点位置）
        x = i / 10
        y = j / 10

        x1 = int(np.floor(x))
        y1 = int(np.floor(y))
        x2 = min(x1 + 1, h - 1)
        y2 = min(y1 + 1, w - 1)

        dx = x - x1
        dy = y - y1

        for ch in range(c):
            Q11 = img[x1,y1,ch]
            Q21 = img[x2,y1,ch]
            Q12 = img[x1,y2,ch]
            Q22 = img[x2,y2,ch]
            value = Q11 * (1 - dx) * (1 - dy) + Q21 * dx * (1 - dy) + Q12 * (1 - dx) * dy + Q22 * dx * dy
            res_linear[i,j,ch] = int(round(value))

cv2.imwrite('linear.jpg', res_linear)
