import cv2
import math
import numpy as np

def log_trans(c,image):
    h,w = image.shape[0],image.shape[1]
    t_img = np.zeros((h,w),dtype=np.float32) # 创建空图像
    for i in range(h):
        for j in range(w):
            t_img[i,j] = c*math.log(1+image[i,j])
    cv2.normalize(t_img,t_img,0,255,cv2.NORM_MINMAX) # 像素值归一化0~255
    return t_img

img = cv2.imread(r'./2.jpg', 0)
t_img = log_trans(1, img)
cv2.imwrite(r'./log_img.jpg', t_img)
cv2.waitKey(0)