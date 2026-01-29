import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置中文字体

def pearl_roundness_measurement(image_path):
    """珍珠圆度测量主函数"""
    # 1. 读取与预处理
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)

    # 2. 轮廓检测与去重
    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = [c for c in contours if cv2.contourArea(c) > 500]
    features = []
    for cnt in valid_contours:
        m = cv2.moments(cnt)
        if m["m00"] == 0: continue
        cx, cy = int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        roundness = 4 * np.pi * area / (perimeter ** 2) if perimeter else 0
        features.append((cnt, cx, cy, area, perimeter, roundness))

    # 3. 自动去重
    sorted_by_area = sorted(features, key=lambda x: x[3], reverse=True)
    distance_threshold = 100
    unique_features = []
    used_indices = set()
    for i in range(len(sorted_by_area)):
        if i in used_indices: continue
        unique_features.append(sorted_by_area[i])
        for j in range(i + 1, len(sorted_by_area)):
            if j in used_indices: continue
            dx = sorted_by_area[i][1] - sorted_by_area[j][1]
            dy = sorted_by_area[i][2] - sorted_by_area[j][2]
            if np.sqrt(dx * dx + dy * dy) < distance_threshold:
                used_indices.add(j)
    filtered_features = unique_features[:8]

    # 4. 按相对位置排序
    def sort_by_relative_position(features):
        """按行列相对位置排序：先分上下行，再左右排序"""
        centers = [(f[1], f[2]) for f in features]
        # 提取所有y坐标，计算中位数作为行列分界
        ys = [cy for (cx, cy) in centers]
        y_median = np.median(ys)

        # 分组：上行为y < 中位数，下行为y >= 中位数
        upper_row = []
        lower_row = []
        for cx, cy in centers:
            if cy < y_median:
                upper_row.append((cx, cy))
            else:
                lower_row.append((cx, cy))

        # 每行按x坐标从左到右排序
        upper_row_sorted = sorted(upper_row, key=lambda x: x[0])
        lower_row_sorted = sorted(lower_row, key=lambda x: x[0])

        # 合并顺序：上一行从左到右，下一行从左到右
        return upper_row_sorted + lower_row_sorted

    # 应用排序并匹配特征
    sorted_centers = sort_by_relative_position(filtered_features)
    sorted_features = []
    for cx, cy in sorted_centers:
        for feat in filtered_features:
            if feat[1] == cx and feat[2] == cy:
                sorted_features.append(feat)
                break

    # 提取结果
    cnts = [f[0] for f in sorted_features]
    centers = [(f[1], f[2]) for f in sorted_features]
    areas = [f[3] for f in sorted_features]
    perimeters = [f[4] for f in sorted_features]
    roundness = [f[5] for f in sorted_features]

    # 5. 生成标记图
    marked_img = img_rgb.copy()
    for i, (cnt, (cx, cy)) in enumerate(zip(cnts, centers)):
        cv2.drawContours(marked_img, [cnt], -1, (0, 255, 0), 3)
        cv2.circle(marked_img, (cx, cy), 40, (0, 0, 255), -1)
        cv2.putText(marked_img, f"P{i + 1}", (cx + 15, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 10, (0, 0, 255), 3, cv2.LINE_AA)

    # 6. 保存图像
    plt.rcParams["figure.dpi"] = 300
    plt.figure(figsize=(8, 6))
    plt.imshow(gray, cmap='gray')
    plt.title('1. 灰度图', fontsize=24)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.imshow(thresh, cmap='gray')
    plt.title('2. 阈值分割结果', fontsize=24)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.imshow(opened, cmap='gray')
    plt.title('3. 形态学处理后', fontsize=24)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    plt.imshow(marked_img)
    plt.title('4. 珍珠标记结果', fontsize=24)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # 7. 输出结果表格
    print("珍珠圆度测量结果（按相对位置排序P1-P8）:")
    print("-" * 70)
    print(f"{'编号':^10}{'中心坐标':^20}{'面积':^15}{'周长':^15}{'圆度':^15}")
    print("-" * 70)
    for i, (cx, cy) in enumerate(centers):
        print(f"P{i + 1:^10}{f'({cx}, {cy})':^20}{areas[i]:^15.2f}{perimeters[i]:^15.2f}{roundness[i]:^15.4f}")
    print("-" * 70)

    return centers, roundness

if __name__ == "__main__":
    image_path = "pearls1.jpg"
    try:
        centers, _ = pearl_roundness_measurement(image_path)
    except Exception as e:
        print(f"处理错误: {e}")