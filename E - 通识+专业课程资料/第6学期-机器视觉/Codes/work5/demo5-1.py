import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置matplotlib显示中文
rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体

# 加载图像
image_path = "2.png"
original_image = cv2.imread(image_path)

# 转换为RGB格式
image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

# 创建处理副本
processed_image = image_rgb.copy()

# 获取图像尺寸
height, width = processed_image.shape[:2]

# 创建眼睛区域掩膜，用于保留睫毛部分
eye_mask = np.zeros((height, width), dtype=np.uint8)

# 粗略估计眼睛区域位置（可根据实际图像调整）
left_eye_region = (int(width * 0.28), int(height * 0.38), int(width * 0.17), int(height * 0.15))
right_eye_region = (int(width * 0.55), int(height * 0.38), int(width * 0.17), int(height * 0.15))

# 在掩膜上绘制白色矩形（表示保留区域）
cv2.rectangle(eye_mask, (left_eye_region[0], left_eye_region[1]),
              (left_eye_region[0] + left_eye_region[2], left_eye_region[1] + left_eye_region[3]), 255, -1)
cv2.rectangle(eye_mask, (right_eye_region[0], right_eye_region[1]),
              (right_eye_region[0] + right_eye_region[2], right_eye_region[1] + right_eye_region[3]), 255, -1)

# 使用高斯模糊进行平滑处理，模拟双线性滤波效果
smoothed_image = cv2.GaussianBlur(processed_image, (11, 11), 0)

# 创建反掩膜，分别处理脸部和睫毛区域
eye_mask_inv = cv2.bitwise_not(eye_mask)
face_part = cv2.bitwise_and(smoothed_image, smoothed_image, mask=eye_mask_inv)
eye_part = cv2.bitwise_and(processed_image, processed_image, mask=eye_mask)
final_image = cv2.add(face_part, eye_part)

# 显示处理结果
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("原始图像")
plt.imshow(image_rgb)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("去雀斑（保留睫毛）")
plt.imshow(final_image)
plt.axis("off")

plt.tight_layout()
plt.show()
