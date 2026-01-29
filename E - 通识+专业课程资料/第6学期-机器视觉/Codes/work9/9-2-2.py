import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] ='SimHei'
template = cv2.imread('egg_template.jpg', cv2.IMREAD_GRAYSCALE)
image = cv2.imread('eggs.png', cv2.IMREAD_GRAYSCALE)

# 创建SIFT特征检测器
sift = cv2.SIFT_create()

# 创建多尺度图像金字塔
def create_pyramid(image, num_scales=4, scale_factor=1.2):
    pyramid = [image]
    for i in range(1, num_scales):
        scaled_image = cv2.resize(image, None, fx=1.0 / scale_factor ** i, fy=1.0 / scale_factor ** i,
                                  interpolation=cv2.INTER_AREA)
        pyramid.append(scaled_image)
    return pyramid


template_pyramid = create_pyramid(template)
image_pyramid = create_pyramid(image)

# 存储所有匹配结果
all_matches = []
all_keypoints_template = []
all_keypoints_image = []
all_descriptors_template = []
all_descriptors_image = []

for i, scaled_template in enumerate(template_pyramid):
    # 检测模板图像和待检测图像中的关键点和描述符
    keypoints_template, descriptors_template = sift.detectAndCompute(scaled_template, None)
    keypoints_image, descriptors_image = sift.detectAndCompute(image_pyramid[i], None)

    # 检查是否检测到关键点
    if keypoints_template is None or keypoints_image is None:
        continue

    # 使用FLANN匹配器进行特征匹配
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # 检查描述符是否存在
    if descriptors_template is None or descriptors_image is None:
        continue

    # 确保描述符有足够的数量进行匹配
    if len(descriptors_template) < 2 or len(descriptors_image) < 2:
        continue

    matches = flann.knnMatch(descriptors_template, descriptors_image, k=2)

    # 使用Lowe的比率测试筛选出好的匹配
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    all_matches.append(good_matches)
    all_keypoints_template.append(keypoints_template)
    all_keypoints_image.append(keypoints_image)
    all_descriptors_template.append(descriptors_template)
    all_descriptors_image.append(descriptors_image)

# 在原始图像上绘制所有匹配结果
image_with_all_boxes = image.copy()
for i, good_matches in enumerate(all_matches):
    if len(good_matches) > 4:
        # 获取当前尺度的关键点
        keypoints_template = all_keypoints_template[i]
        keypoints_image = all_keypoints_image[i]

        # 检查关键点数量是否足够
        if len(keypoints_template) == 0 or len(keypoints_image) == 0:
            continue

        src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_image[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 调整尺度
        scale_factor = 1.2 ** i
        src_pts *= scale_factor
        dst_pts *= scale_factor

        # 计算单应性矩阵
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        if M is not None:
            # 计算模板图像的边界在图像上的位置
            h, w = template.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            # 在图像上绘制边框
            image_with_all_boxes = cv2.polylines(image_with_all_boxes, [np.int32(dst)], True, (0, 0, 255), 2,
                                                 cv2.LINE_AA)

# 保存结果图像
cv2.imwrite('result.png', image_with_all_boxes)

# 使用Matplotlib显示匹配结果
plt.imshow(image_with_all_boxes, cmap='gray')
plt.title('多尺度金字塔匹配 Matches with Multi-scale Pyramid')
plt.show()