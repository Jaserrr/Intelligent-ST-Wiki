import cv2
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
gray_img = cv2.imread('document.bmp', cv2.IMREAD_GRAYSCALE)

# 先进行二值化
_, binary_mask = cv2.threshold(gray_img, 100, 1, cv2.THRESH_BINARY_INV)
binary_mask = (binary_mask * 255).astype('uint8')

# 提取字母“l”（在倒数第三个找到一个相对清晰的）
letter_l = binary_mask[405:425, 34:39]
letter_l_inv = cv2.bitwise_not(letter_l)

# 命中-未命中变换（Hit-or-Miss）
erosion_fg = cv2.erode(binary_mask, letter_l)
erosion_bg = cv2.erode(cv2.bitwise_not(binary_mask), letter_l_inv)
hitmiss_result = cv2.bitwise_and(erosion_fg, erosion_bg)

# 使用“l”结构元素进行膨胀
letter_l_flip = cv2.flip(letter_l, -1)
dilated_result = cv2.dilate(hitmiss_result, letter_l_flip, anchor=(0, 0))

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title('二值图像（反转）')
plt.imshow(binary_mask, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('提取字母“l”结果')
plt.imshow(dilated_result, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()
