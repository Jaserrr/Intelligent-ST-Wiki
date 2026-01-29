import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'SimHei'

img = Image.open('3-2.png').convert('L')
img_array = np.array(img)

# 傅里叶变换并中心化
fft = np.fft.fft2(img_array)
fft_shift = np.fft.fftshift(fft)

# 计算对数幅度谱（用于观察）
magnitude_spectrum = 20 * np.log(np.abs(fft_shift) + 1e-6)

# 图像尺寸参数
rows, cols = img_array.shape
crow, ccol = rows//2, cols//2  # 中心坐标

# 滤波器参数（根据频谱图调整）
delta_x = 28     # 条纹频率距中心的水平距离
w = 18   # 滤波区域宽度
h = 2    # 滤波区域高度

# 创建全通掩膜
mask = np.ones((rows, cols), dtype=np.uint8)

# 在正负频率位置创建矩形滤波区域
mask[crow-h:crow+h, ccol+delta_x-w:ccol+delta_x+w] = 0
mask[crow-h:crow+h, ccol-delta_x-w:ccol-delta_x+w] = 0

# 应用掩膜
fft_shift_filtered = fft_shift * mask

# 逆变换回空间域
fft_ishift = np.fft.ifftshift(fft_shift_filtered)
img_filtered = np.fft.ifft2(fft_ishift)
img_filtered = np.abs(img_filtered).astype(np.uint8)

Image.fromarray(img_filtered).save('result.png')

plt.figure(figsize=(12,4))
plt.subplot(131), plt.imshow(img_array, cmap='gray'), plt.title('原图')
plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('频域')
plt.subplot(133), plt.imshow(img_filtered, cmap='gray'), plt.title('去条纹结果')
plt.show()