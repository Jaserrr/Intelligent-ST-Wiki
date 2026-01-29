import cv2
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题


# ---------------------- 1. 图像读取与初始预处理 ----------------------
def read_and_preprocess():
    """读取图像并进行阈值分割、形态学操作"""
    gray = cv2.imread('14raw.bmp', cv2.IMREAD_GRAYSCALE)
    original = cv2.imread('14raw.bmp')
    if gray is None or original is None:
        raise FileNotFoundError("未能成功读取 14raw.bmp 文件，请检查文件路径和名称")

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = 255 - binary
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return gray, original, binary


# ---------------------- 2. 工件分割与可视化 ----------------------
def segment_parts(gray, original, binary):
    """分割工件并绘制边界框、大号编号、加粗中心点"""
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 1000
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    bounding_boxes = [cv2.boundingRect(cnt) for cnt in valid_contours]
    bounding_boxes.sort(key=lambda box: box[1])

    parts = []
    for i, (x, y, w, h) in enumerate(bounding_boxes):
        padding = 10
        x1, y1 = max(x - padding, 0), max(y - padding, 0)
        x2, y2 = min(x + w + padding, gray.shape[1]), min(y + h + padding, gray.shape[0])
        parts.append(gray[y1:y2, x1:x2])

        cv2.rectangle(original, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(original, f'{i + 1}', (x1 + 10, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

        center_x, center_y = x1 + (x2 - x1) // 2, y1 + (y2 - y1) // 2
        cv2.circle(original, (center_x, center_y), 8, (0, 0, 255), -1)
        print(f"工件 {i + 1} 中心点: ({center_x}, {center_y})")

    plt.figure(figsize=(12, 10))
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("工件标记（加粗点+大号编号）")
    plt.axis('off')
    plt.show()

    return parts


# ---------------------- 3. 单个工件处理函数 ----------------------
def process_single_part(part_gray, part_idx, pixel_size_y=0.025):
    """处理单个工件并计算实际距离"""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    gray_enhanced = clahe.apply(part_gray)
    gray_enhanced = cv2.GaussianBlur(gray_enhanced, (5, 5), 0)

    sobelx = cv2.Sobel(gray_enhanced, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(gray_enhanced, cv2.CV_64F, 0, 1, ksize=5)
    sobel_magnitude = 0.5 * np.abs(sobelx) + 0.5 * np.abs(sobely)
    sobel_magnitude = np.uint8(255 * sobel_magnitude / np.max(sobel_magnitude))
    _, edge_binary = cv2.threshold(sobel_magnitude, 15, 255, cv2.THRESH_BINARY)

    edges = edge_binary.copy()

    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=50,
                            minLineLength=200, maxLineGap=10)

    horizontal_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx, dy = abs(x2 - x1), abs(y2 - y1)
            if dx > dy and dy < 5:  # 水平直线
                y_avg = int((y1 + y2) / 2)
                horizontal_lines.append((y_avg, min(x1, x2), max(x1, x2)))

    horizontal_lines.sort(key=lambda l: l[0])

    merged_lines = []
    merge_threshold = 10
    for y, x_start, x_end in horizontal_lines:
        if not merged_lines:
            merged_lines.append([y, x_start, x_end])
        else:
            last_y, last_x_start, last_x_end = merged_lines[-1]
            if abs(y - last_y) < merge_threshold:
                new_y = int((last_y + y) / 2)
                new_x_start = min(last_x_start, x_start)
                new_x_end = max(last_x_end, x_end)
                merged_lines[-1] = [new_y, new_x_start, new_x_end]
            else:
                merged_lines.append([y, x_start, x_end])

    # 绘制结果
    line_img = cv2.cvtColor(part_gray, cv2.COLOR_GRAY2BGR)
    for y, x_start, x_end in merged_lines:
        cv2.line(line_img, (x_start, y), (x_end, y), (0, 255, 0), 2)

    plt.figure(figsize=(8, 6))
    plt.imshow(cv2.cvtColor(line_img, cv2.COLOR_BGR2RGB))
    plt.title(f"工件 {part_idx + 1} 合并后的水平直线")
    plt.axis('off')
    plt.show()

    # 计算并返回y坐标
    line_ys = [line[0] for line in merged_lines]
    line_ys.sort()

    return line_ys


# ---------------------- 4. 主程序流程 ----------------------
if __name__ == "__main__":
    # 读取并预处理图像
    gray, original, binary = read_and_preprocess()

    # 分割工件
    parts = segment_parts(gray, original, binary)

    # 处理每个工件并收集y坐标
    all_line_ys = []
    for idx, part in enumerate(parts):
        line_ys = process_single_part(part, idx)
        all_line_ys.append(line_ys)
        print(f"工件 {idx + 1} 的y坐标:", line_ys)

    # 将y坐标与序号关联（根据实际情况调整）
    # 假设工件1-4的y坐标分别对应序号: 444, 445, 447, 448, 442, 443
    # 这里需要根据实际检测到的工件数量和y坐标顺序调整映射关系
    if len(all_line_ys) >= 6:
        # 假设前6个y坐标分别对应序号444-448,442,443
        y_to_id = {
            all_line_ys[0][0]: 444,
            all_line_ys[1][0]: 445,
            all_line_ys[2][0]: 447,
            all_line_ys[3][0]: 448,
            all_line_ys[4][0]: 442,
            all_line_ys[5][0]: 443
        }

        # 计算指定序号对之间的距离
        distance_pairs = [
            (442, 443),
            (445, 448),
            (444, 445),
            (447, 448)
        ]

        print("\n===== 指定序号对之间的距离 =====")
        for pair in distance_pairs:
            id1, id2 = pair
            y1 = [y for y, i in y_to_id.items() if i == id1][0]
            y2 = [y for y, i in y_to_id.items() if i == id2][0]
            pixel_distance = abs(y1 - y2)
            actual_distance = pixel_distance * 0.025  # 垂直方向单位像素尺寸

            print(f"{id1}-{id2} 的像素距离: {pixel_distance}")
            print(f"{id1}-{id2} 的实际距离(mm): {actual_distance:.3f}")
            print("-" * 30)
    else:
        print("警告：检测到的工件数量不足，无法完成序号映射和距离计算")