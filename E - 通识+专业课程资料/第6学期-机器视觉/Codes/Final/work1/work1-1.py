import cv2
image = cv2.imread('14raw.bmp', cv2.IMREAD_GRAYSCALE)

_, thresholded = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV) # 应用二值化阈值
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # 查找图像中的轮廓
center = [] # 存储中心点

for contour in contours: # 遍历所有轮廓,分别求中心点
    M = cv2.moments(contour) # 计算轮廓的矩
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0

    center.append((cX, cY)) # 将中心点添加到列表中
    cv2.circle(image, (cX, cY), 10, (255, 0, 0), -1) # 在图像上绘制中心点

center.sort(key=lambda point: point[1])

for i, point in enumerate(center[1:]):
    print(f"元件 {i+1} 的中心点坐标: {point}")

cv2.imwrite('center.jpg',image)
