import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']

img_color = cv2.imread("cats.jpg")
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

template_color = cv2.imread("cats template.jpg")
template_gray = cv2.cvtColor(template_color, cv2.COLOR_BGR2GRAY)

def compute_gradient(img):
    Gx = np.zeros_like(img, dtype=np.float32)
    Gy = np.zeros_like(img, dtype=np.float32)
    Gx[:, 1:-1] = img[:, 2:] - img[:, :-2]
    Gy[1:-1, :] = img[2:, :] - img[:-2, :]
    magnitude = np.sqrt(Gx**2 + Gy**2)
    return Gx, Gy, magnitude

# 模板梯度
gx_tpl, gy_tpl, mag_tpl = compute_gradient(template_gray)

# 模板大小
h, w = template_gray.shape

# ========== 进行滑动窗口匹配 ==========
max_score = -np.inf
best_x, best_y = 0, 0

# 遍历原图中的所有可能位置（逐像素滑动）
for y in range(0, img_gray.shape[0] - h):
    for x in range(0, img_gray.shape[1] - w):
        patch = img_gray[y:y+h, x:x+w]
        gx_p, gy_p, mag_p = compute_gradient(patch)

        # 使用方向余弦相似度作为匹配指标（越大越相似）
        score = np.sum(np.cos(gx_tpl - gx_p) * mag_tpl * mag_p)

        if score > max_score:
            max_score = score
            best_x, best_y = x, y
            best_gx, best_gy, best_mag = gx_p, gy_p, mag_p

matched_img = img_color.copy()
cv2.rectangle(matched_img, (best_x, best_y), (best_x + w, best_y + h), (0, 255, 0), 2)

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("HOG模板匹配流程图", fontsize=18)

# 上排：原图 / 模板 / 匹配结果
axes[0, 0].imshow(cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB))
axes[0, 0].set_title("原始图像 cats.jpg")
axes[0, 0].axis('off')

axes[0, 1].imshow(template_gray, cmap='gray')
axes[0, 1].set_title("模板图像 cats template.jpg")
axes[0, 1].axis('off')

axes[0, 2].imshow(cv2.cvtColor(matched_img, cv2.COLOR_BGR2RGB))
axes[0, 2].set_title("匹配结果（绿色框）")
axes[0, 2].axis('off')

# 下排：水平梯度 / 垂直梯度 / 梯度幅值
axes[1, 0].imshow(best_gx, cmap='gray')
axes[1, 0].set_title("匹配区域 - Gx（水平方向梯度）")
axes[1, 0].axis('off')

axes[1, 1].imshow(best_gy, cmap='gray')
axes[1, 1].set_title("匹配区域 - Gy（垂直方向梯度）")
axes[1, 1].axis('off')

axes[1, 2].imshow(best_mag, cmap='gray')
axes[1, 2].set_title("匹配区域 - Magnitude（梯度幅值）")
axes[1, 2].axis('off')

plt.tight_layout()
plt.show()
