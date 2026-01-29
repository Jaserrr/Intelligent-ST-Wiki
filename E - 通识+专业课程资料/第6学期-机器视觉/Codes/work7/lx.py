import cv2
import os
# 1. 读取图像（灰度模式）
img = cv2.imread('document.bmp', cv2.IMREAD_GRAYSCALE)

# 2. 二值化处理（阈值可以根据需要调整）
# THRESH_BINARY_INV: 让黑色的字母变为前景（值为1）
_, binary = cv2.threshold(img, 100, 1, cv2.THRESH_BINARY_INV)
binary= (binary * 255).astype('uint8')
path=''
filename = os.path.join(path,"new_image1.jpg")
cv2.imwrite(filename, binary)

l= binary[405:425, 34:39]

# 4. 显示截取的区域
cv2.imshow("Region of Interest", l)
cv2.waitKey(0)
cv2.destroyAllWindows()

l_fan=cv2.bitwise_not(l)

qinshi1 = cv2.erode(binary,l)
qinshi2 = cv2.erode(cv2.bitwise_not(binary), l_fan)

hit_or_miss = cv2.bitwise_and(qinshi1, qinshi2)

l=cv2.flip(l, -1)
result=cv2.dilate(hit_or_miss, l, anchor=(0, 0))
cv2.imshow('1',result)
cv2.imshow('2',binary)
cv2.waitKey(0)
cv2.destroyAllWindows()