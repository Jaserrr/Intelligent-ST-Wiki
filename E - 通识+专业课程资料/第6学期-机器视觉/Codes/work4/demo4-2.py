import cv2
import numpy as np

def homo(img, d0=10, rl=0.5, rh=2.5, c=2, h=2.0, l=0.5):
    img_log = np.log(img + 1e-5)      # 加上极小数防止 log(0) 报错
    rows, cols = img_log.shape
    Z = np.fft.fft2(img_log)          # 傅里叶变换 (FFT)
    Z = np.fft.fftshift(Z)            # FFT 中心化
    M, N = np.meshgrid(np.arange(-cols // 2, cols // 2), np.arange(-rows // 2, rows // 2))
    D = np.sqrt(M ** 2 + N ** 2)      # 计算欧氏距离

    # 频域滤波器 H(u,v)
    H = (rh - rl) * (1 - np.exp(-c * (D ** 2 / d0 ** 2))) + rl
    S = H * Z
    S = (h - l) * S + l              # 线性缩放并平移，控制滤波器的斜率

    img_s = np.fft.ifftshift(S)      # IFFT 逆中心化，撤销 fftshift 操作
    img_s = np.fft.ifft2(img_s)      # 傅里叶反变换(IFFT)
    img_g = np.real(img_s)           # IFFT 取实部

    img_g = np.exp(img_g) - 1        # 还原
    img_g = np.uint8(np.clip(img_g, 0, 255))
    return img_g

img = cv2.imread('2.png', cv2.IMREAD_GRAYSCALE)
img_new = homo(img)

cv2.imwrite("img_new.png", img_new)
cv2.waitKey(0)

