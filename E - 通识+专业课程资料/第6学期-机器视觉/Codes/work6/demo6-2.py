import cv2
import numpy as np
from sklearn.cluster import DBSCAN

def draw_line_rho_theta(img, rho, theta, color=(0, 0, 255), thickness=2):
    """根据 rho 和 theta 绘制整条直线（长度足够长）"""
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    # 画一条足够长的直线（跨越图像）
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def detect_blue_lines(image_path, output_path="3.png"):
    # 读取图像
    img = cv2.imread(image_path)
    out_img = img.copy()

    # 提取蓝色区域
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # 边缘检测
    edges = cv2.Canny(mask, 50, 150)

    # Hough Transform (标准版本)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

    if lines is not None:
        # 提取 rho 和 theta
        features = np.array([[l[0][0], l[0][1]] for l in lines])

        # 归一化角度在 [0, π)
        features[:, 1] = features[:, 1] % np.pi

        # 角度和位置缩放后聚类
        angle_eps = np.deg2rad(3)
        rho_eps = 15
        scaled = np.copy(features)
        scaled[:, 0] /= rho_eps
        scaled[:, 1] /= angle_eps

        # 聚类合并重复线
        db = DBSCAN(eps=1.2, min_samples=1).fit(scaled)
        labels = db.labels_

        n_lines = len(np.unique(labels))
        print(f"检测到蓝色线条：{n_lines}")

        # 为每个类别绘制一条线（用平均ρ、θ）
        for label in np.unique(labels):
            group = features[labels == label]
            mean_rho = np.mean(group[:, 0])
            mean_theta = np.mean(group[:, 1])
            draw_line_rho_theta(out_img, mean_rho, mean_theta)

    else:
        print("未检测到蓝色线条。")
        n_lines = 0

    # 保存图像
    cv2.imwrite(output_path, out_img)
    print(f"输出图像已保存为: {output_path}")
    return n_lines

if __name__ == "__main__":
    detect_blue_lines("1.png")
