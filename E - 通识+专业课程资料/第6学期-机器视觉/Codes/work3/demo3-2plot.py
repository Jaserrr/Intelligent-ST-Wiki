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

# 手动设置滤波器参数（需要根据频谱图调整）
delta_x = 28     # 条纹频率距中心的水平距离
mask_width = 16   # 滤波区域宽度
mask_height = 2    # 滤波区域高度

# 创建全通掩膜
mask = np.ones((rows, cols), dtype=np.uint8)

# 在正负频率位置创建矩形滤波区域
mask[crow-mask_height:crow+mask_height,
     ccol+delta_x-mask_width:ccol+delta_x+mask_width] = 0
mask[crow-mask_height:crow+mask_height,
     ccol-delta_x-mask_width:ccol-delta_x+mask_width] = 0

# 应用掩膜
fft_shift_filtered = fft_shift * mask

# 逆变换回空间域
fft_ishift = np.fft.ifftshift(fft_shift_filtered)
img_filtered = np.fft.ifft2(fft_ishift)
img_filtered = np.abs(img_filtered).astype(np.uint8)

# 保存结果
Image.fromarray(img_filtered).save('filtered_result.jpg')

spectrum_display = np.log(np.abs(fft_shift))  # 对数变换增强显示
spectrum_display = (spectrum_display - spectrum_display.min()) / (spectrum_display.max() - spectrum_display.min())  # 归一化
plt.imshow(spectrum_display, cmap='gray')
plt.title('对数幅度谱（中心化）')
plt.axvline(x=ccol, color='r', linestyle='--', linewidth=0.5)  # 中心竖线
plt.axhline(y=crow, color='r', linestyle='--', linewidth=0.5)  # 中心横线
plt.colorbar(label='强度')
plt.tight_layout()
plt.show()