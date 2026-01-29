import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示

# 加载图像
image = cv2.imread("2.png")

# 将图像从BGR转为RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 使用Haar Cascade分类器加载面部特征检测器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# 将图像转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 检测脸部
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# 创建一个全黑的掩膜
eyes_only_mask = np.zeros_like(image)

# 提取面部区域并标记眼睛区域
for (x, y, w, h) in faces:
    roi_gray = gray[y:y + h, x:x + w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    # 在眼睛区域保留细节！！
    for (ex, ey, ew, eh) in eyes:
        eyes_only_mask[y + ey:y + ey + eh, x + ex:x + ex + ew] = 255  # 保留眼睛区域

# 对图像应用双边滤波
bilateral_filtered = cv2.bilateralFilter(image, d=15, sigmaColor=75, sigmaSpace=75)

# 将眼睛区域从原图复制到处理后的图像
final_image = np.copy(bilateral_filtered)
final_image[eyes_only_mask == 255] = image[eyes_only_mask == 255]

# 显示并保存处理后的图像
cv2.imshow("Processed Image", final_image)
cv2.imwrite("processed_image.png", final_image)

# 等待用户按键然后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()