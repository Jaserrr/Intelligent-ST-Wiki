import cv2
import math
import numpy as np

def gamma(c,gamma,image):
    h,w = image.shape[0],image.shape[1]
    t_img = np.zeros((h,w),dtype=np.float32) # 创建空图像
    for i in range(h):
        for j in range(w):
            t_img[i,j] = c*math.pow(image[i,j], gamma)
    cv2.normalize(t_img,t_img,0,255,cv2.NORM_MINMAX) # 像素值归一化0~255
    return t_img

img = cv2.imread(r'./1.jpg', 0)
t_img = gamma(1, 0.5, img)
cv2.imwrite(r'./gamma1.jpg', t_img)
cv2.waitKey(0)