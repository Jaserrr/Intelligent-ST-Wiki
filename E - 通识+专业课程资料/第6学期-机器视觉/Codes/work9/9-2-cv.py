import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] ='SimHei'
template = cv2.imread('egg_template.jpg', cv2.IMREAD_GRAYSCALE)
image = cv2.imread('eggs.png', cv2.IMREAD_GRAYSCALE)

# 创建SIFT特征检测器
sift = cv2.SIFT_create()

# 检测模板图像和待检测图像中的关键点和描述符
keypoints_template, descriptors_template = sift.detectAndCompute(template, None)
keypoints_image, descriptors_image = sift.detectAndCompute(image, None)

# 使用FLANN匹配器进行特征匹配
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(descriptors_template, descriptors_image, k=2)

# 使用Lowe的比率测试筛选出好的匹配
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# 如果找到了足够的匹配点，则计算单应性矩阵并绘制匹配结果
if len(good_matches) > 4:
    src_pts = np.float32([keypoints_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints_image[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    matches_mask = mask.ravel().tolist()

    # 计算模板图像的边界在图像上的位置
    h, w = template.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    # 在图像上绘制边框
    image_with_box = cv2.polylines(image, [np.int32(dst)], True, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imwrite('result.png', image_with_box)
else:
    print("Not enough matches are found - {}/{}".format(len(good_matches), 4))

# 使用Matplotlib显示匹配结果
result_image = cv2.drawMatches(template, keypoints_template, image, keypoints_image, good_matches, None, flags=2)
plt.imshow(result_image, cmap='gray')
plt.title('SIFT方法进行匹配')
plt.show()