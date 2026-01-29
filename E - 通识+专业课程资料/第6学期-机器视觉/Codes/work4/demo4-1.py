import cv2
import numpy as np

def Calculate_H(R, G, B):
    a = 0.5 * ((R - G) + (R - B))
    b = np.sqrt((R - G) ** 2 + (R - B) * (G - B)) + 1e-6
    theta = np.arccos(a/b)
    H = np.degrees(theta) / 360.0
    np.putmask(H, B > G, (360 - np.degrees(theta)) / 360.0)
    H[b <= 1e-6] = 0 # 分母为极小值，还原为0
    return H

def Calculate_S(R, G, B):
    I = (R + G + B) / 3.0
    min_val = np.minimum(np.minimum(R, G), B)
    return np.where(I > 1e-6, 1 - min_val / (I + 1e-6), 0) # 防止分母为0

def RGB2HSI(rgb_img):
    B, G, R = cv2.split(rgb_img/255.0)
    H = Calculate_H(R, G, B)
    S = Calculate_S(R, G, B)
    I = (R + G + B) / 3.0
    # 合并通道
    return np.clip(cv2.merge([H*255,S*255,I*255]), 0, 255).astype(np.uint8)


def HSI2RGB(hsi_img):
    H, S, I = cv2.split(hsi_img/255.0)
    H = H * 360  # 转换为角度制
    sec = np.floor(H/120).astype(int)%3   # 分段，sec取0,1,2
    H=H-120*sec  # sec取1/2分别先减掉120/240
    cos_H = np.cos(np.radians(H))
    cos_60_H = np.cos(np.radians(60-H))
    Z = I*(1+S*cos_H/np.maximum(cos_60_H,1e-6)) # 防止分母为0

    # 初始化RGB通道
    R = np.zeros_like(I)
    G = np.zeros_like(I)
    B = np.zeros_like(I)

    # 扇区0: 0°-120°
    mask0 = (sec == 0)
    R[mask0] = Z[mask0]
    B[mask0] = I[mask0] * (1 - S[mask0])
    G[mask0] = 3 * I[mask0] - (R[mask0] + B[mask0])

    # 扇区1: 120°-240°
    mask1 = (sec == 1)
    G[mask1] = Z[mask1]
    R[mask1] = I[mask1] * (1 - S[mask1])
    B[mask1] = 3 * I[mask1] - (R[mask1] + G[mask1])

    # 扇区2: 240°-360°
    mask2 = (sec == 2)
    B[mask2] = Z[mask2]
    G[mask2] = I[mask2] * (1 - S[mask2])
    R[mask2] = 3 * I[mask2] - (G[mask2] + B[mask2])

    # 合并通道，并转换回0-255范围
    rgb_img = np.clip(cv2.merge([B * 255, G * 255, R * 255]), 0, 255).astype(np.uint8)
    return rgb_img

def average_filter(hsi_img,d):
    hsi_img[:, :, d] = cv2.blur(hsi_img[:, :, d], (25, 25))
    return hsi_img

rgb_img = cv2.imread('image1.bmp', cv2.IMREAD_COLOR)
hsi_img = RGB2HSI(rgb_img)
hsi_img_blur = average_filter(hsi_img,0) # d=0为第一维，即H
rgb_img2 = HSI2RGB(hsi_img_blur)
cv2.imwrite("HSI.jpeg", hsi_img)
cv2.imwrite("RGB.jpeg", rgb_img2)
cv2.waitKey(0)