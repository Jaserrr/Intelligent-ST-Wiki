import cv2

img = cv2.imread('Snoopy-small.jpg')

# 放大尺寸
scale_factor = 10
height, width = img.shape[:2]
new_size = (int(width * scale_factor), int(height * scale_factor))

# 最近邻插值
res_nearest = cv2.resize(img, new_size, interpolation=cv2.INTER_NEAREST)
cv2.imwrite('1_nearest.jpg', res_nearest)

# 双线性插值
res_linear = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
cv2.imwrite('1_linear.jpg', res_linear)