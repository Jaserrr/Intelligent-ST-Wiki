import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, sobel
from scipy.spatial.distance import cdist

# 加载图像并转换为灰度
def load_grayscale_image(path):
    img = Image.open(path).convert('L')  # 转灰度
    return np.array(img, dtype=np.float32) / 255.0

# 计算DoG金字塔
def build_dog_pyramid(image, num_scales=5, sigma=1.6, k=1.4):
    gaussian_pyramid = [gaussian_filter(image, sigma * (k**i)) for i in range(num_scales)]
    dog_pyramid = [gaussian_pyramid[i+1] - gaussian_pyramid[i] for i in range(num_scales - 1)]
    return dog_pyramid

# 查找关键点（极值点）
def find_keypoints(dog_pyramid, threshold=0.02):
    keypoints = []
    for i in range(1, len(dog_pyramid)-1):
        dog_prev, dog, dog_next = dog_pyramid[i-1:i+2]
        for y in range(1, dog.shape[0]-1):
            for x in range(1, dog.shape[1]-1):
                patch = np.stack([dog_prev[y-1:y+2,x-1:x+2], dog[y-1:y+2,x-1:x+2], dog_next[y-1:y+2,x-1:x+2]])
                val = dog[y,x]
                if np.abs(val) > threshold and (val == patch.max() or val == patch.min()):
                    keypoints.append((x, y))
    return np.array(keypoints)

# 计算梯度描述子（简单版）
def compute_descriptors(image, keypoints):
    descriptors = []
    for x, y in keypoints:
        if x < 4 or y < 4 or x > image.shape[1]-5 or y > image.shape[0]-5:
            continue
        patch = image[y-4:y+5, x-4:x+5]
        gx = sobel(patch, axis=1)
        gy = sobel(patch, axis=0)
        magnitude = np.sqrt(gx**2 + gy**2)
        descriptor = magnitude.flatten()
        descriptor /= np.linalg.norm(descriptor) + 1e-7
        descriptors.append(descriptor)
    return np.array(descriptors)

# 特征匹配
def match_descriptors(desc1, desc2, threshold=0.6):
    distances = cdist(desc1, desc2, 'euclidean')
    matches = []
    for i, dists in enumerate(distances):
        min_idx = np.argmin(dists)
        if dists[min_idx] < threshold:
            matches.append((i, min_idx))
    return matches

# 加载图像
img1 = load_grayscale_image("egg_template.jpg")
img2 = load_grayscale_image("eggs.png")

# 构建DoG金字塔并检测关键点
dog1 = build_dog_pyramid(img1)
dog2 = build_dog_pyramid(img2)
kp1 = find_keypoints(dog1)
kp2 = find_keypoints(dog2)

# 计算描述子
desc1 = compute_descriptors(img1, kp1)
desc2 = compute_descriptors(img2, kp2)

# 匹配特征点
matches = match_descriptors(desc1, desc2)

# 可视化匹配（示意）
def show_matches(img1, kp1, img2, kp2, matches):
    h1, w1 = img1.shape
    h2, w2 = img2.shape
    canvas = np.zeros((max(h1, h2), w1 + w2))
    canvas[:h1, :w1] = img1
    canvas[:h2, w1:] = img2
    plt.imshow(canvas, cmap='gray')
    for i, j in matches:
        x1, y1 = kp1[i]
        x2, y2 = kp2[j]
        plt.plot([x1, x2 + w1], [y1, y2], 'r', linewidth=0.5)
    plt.axis('off')
    plt.title("SIFT-like Feature Matches (NumPy-only)")
    plt.show()

# 显示匹配结果
show_matches(img1, kp1, img2, kp2, matches)
