import cv2
import numpy as np
from sklearn.cluster import KMeans

def detect_and_draw_coins_v2(image_path, output_path="2.png"):
    img = cv2.imread(image_path)
    out_img = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)
    edges = cv2.Canny(blurred, 80, 150)

    # Hough 圆检测（调整参数以减少误检）
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=100,
        param2=35,  # 更严格的圆形识别
        minRadius=20,
        maxRadius=60
    )

    coin_counts = {}
    if circles is not None:
        circles = np.uint16(np.around(circles[0]))

        # 过滤：基于边缘密度
        valid_circles = []
        for x, y, r in circles:
            mask = np.zeros_like(gray)
            cv2.circle(mask, (x, y), r, 255, 2)
            edge_pixels = cv2.countNonZero(cv2.bitwise_and(edges, edges, mask=mask))
            edge_density = edge_pixels / (2 * np.pi * r)
            if edge_density > 0.4:  # 调整此阈值过滤误圈
                valid_circles.append((x, y, r))

        if not valid_circles:
            print("未检测到有效的硬币圆形。")
            return

        # KMeans 聚类半径
        radii = [r for (_, _, r) in valid_circles]
        radii_np = np.array(radii).reshape(-1, 1)
        kmeans = KMeans(n_clusters=4, random_state=0).fit(radii_np)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_.flatten()

        # 标签映射（小→大）
        sorted_idx = np.argsort(centers)
        label_remap = np.zeros_like(sorted_idx)
        for new_label, old_label in enumerate(sorted_idx):
            label_remap[old_label] = new_label
        final_labels = [label_remap[l] for l in labels]

        # 彩色标注
        color_palette = {
            0: (0, 0, 255),  # 红
            1: (0, 255, 0),  # 绿
            2: (255, 0, 0),  # 蓝
            3: (0, 255, 255)  # 黄
        }

        # 绘图与统计
        for idx, (x, y, r) in enumerate(valid_circles):
            lbl = final_labels[idx]
            color = color_palette.get(lbl, (255, 255, 255))
            cv2.circle(out_img, (x, y), r, color, 2)
            cv2.circle(out_img, (x, y), 2, color, 3)
            coin_counts[lbl] = coin_counts.get(lbl, 0) + 1

    else:
        print("未检测到任何圆。")

    cv2.imwrite(output_path, out_img)
    print("最终有效硬币分类及个数：")
    for lbl in sorted(coin_counts.keys()):
        print(f"  类别 {lbl} ：{coin_counts[lbl]} 个")
    print(f"输出图像已保存为：{output_path}")


if __name__ == "__main__":
    detect_and_draw_coins_v2("1.png")
