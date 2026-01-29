import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设黑体，解决中文显示问题

# ---------------------- 1. 预处理 ----------------------
def preprocess():
    gray = cv2.imread('14raw.bmp', cv2.IMREAD_GRAYSCALE) # 转灰度
    original = cv2.imread('14raw.bmp') # 原图

    # 使用OTSU算法进行自适应阈值分割，自动确定最佳阈值
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    binary = 255 - binary  # 黑白反转，使前景工件为白色
    # 创建5x5矩形结构元素，用于形态学操作
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # 形态学闭操作：先膨胀后腐蚀，填充小孔洞并连接相邻区域
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return gray, original, binary

# ---------------------- 2. 工件分割与可视化 ----------------------
def segment_parts(gray, original, binary):
    """
    查找轮廓并分割出每个工件区域，计算中心点并可视化在原图上
    参数：gray（灰度图）、original（原始彩色图）、binary（二值化图）
    返回：存储每个工件灰度图的列表 parts
    """
    # 查找二值图像中的外部轮廓
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = 1000  # 最小轮廓面积阈值，过滤掉噪声和小区域
    valid_contours = []
    # 筛选有效工件轮廓
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            valid_contours.append(cnt)

    # 计算每个有效轮廓的边界矩形
    boxes = [cv2.boundingRect(cnt) for cnt in valid_contours]
    boxes.sort(key=lambda box: box[1])  # 按 y 坐标排序，确保从上到下排列工件

    parts = []
    # 处理每个工件区域
    for i, (x, y, w, h) in enumerate(boxes):
        padding = 10  # 边界扩展像素数
        # 计算带padding的区域边界，确保不超出图像范围
        x1 = max(x - padding, 0)
        y1 = max(y - padding, 0)
        x2 = min(x + w + padding, gray.shape[1])
        y2 = min(y + h + padding, gray.shape[0])
        # 提取工件区域的灰度图像
        part_img = gray[y1:y2, x1:x2]
        parts.append(part_img)

        # 在原始彩色图上标记工件：绘制边界框、编号和中心点
        cv2.rectangle(original, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(original, f'{i + 1}', (x1 + 10, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 12, (0, 0, 255), 3, cv2.LINE_AA)
        center_x = x1 + (x2 - x1) // 2
        center_y = y1 + (y2 - y1) // 2
        cv2.circle(original, (center_x, center_y), 20, (0, 0, 255), -1)
        print(f"工件 {i+1} 的中心点坐标: ({center_x}, {center_y})")
    print("——" * 20)

    # 可视化工件在原图中的位置
    plt.figure()
    plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
    plt.title("四个工件的中心点位置标注")
    plt.axis('off')
    plt.show()

    return parts

# ---------------------- 3. 单个工件处理函数（增强、边缘检测、霍夫变换、合并直线） ----------------------
def process_single_part(part_gray, idx):
    """
    对单个工件灰度图进行处理：增强、边缘检测、霍夫变换检测直线、合并直线并可视化结果
    参数：part_gray（单个工件的灰度图）、part_idx（工件索引，从 0 开始）
    """
    # 自适应直方图均衡化，增强图像对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    gray_enhanced = clahe.apply(part_gray)
    # 高斯模糊降噪，平滑图像
    gray_enhanced = cv2.GaussianBlur(gray_enhanced, (5, 5), 0)

    # 使用Sobel算子进行边缘检测
    sobelx = cv2.Sobel(gray_enhanced, cv2.CV_64F, 1, 0, ksize=5)  # x方向梯度
    sobely = cv2.Sobel(gray_enhanced, cv2.CV_64F, 0, 1, ksize=5)  # y方向梯度
    # 计算梯度幅值，结合x和y方向梯度
    sobel_magnitude = 0.5 * np.abs(sobelx) + 0.5 * np.abs(sobely)
    # 归一化并转换为8位无符号整数
    sobel_magnitude = np.uint8(255 * sobel_magnitude / np.max(sobel_magnitude))
    # 阈值处理，提取显著边缘
    _, edge_binary = cv2.threshold(sobel_magnitude, 15, 255, cv2.THRESH_BINARY)

    edges = edge_binary.copy()

    # 使用概率霍夫变换检测直线
    lines = cv2.HoughLinesP(edges,
                            rho=1,               # 距离精度（像素）
                            theta=np.pi / 180,   # 角度精度（弧度）
                            threshold=50,        # 最小投票数，阈值越高检测越严格
                            minLineLength=200,   # 最小线段长度
                            maxLineGap=10)       # 线段连接最大间隙

    # 提取并合并水平直线
    splines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            dx = abs(x2 - x1)
            dy = abs(y2 - y1)
            # 判断是否为近似水平直线（x方向变化远大于y方向）
            if dx > dy and dy < 5:
                y_avg = int((y1 + y2) / 2)
                splines.append((y_avg, min(x1, x2), max(x1, x2)))
    splines.sort(key=lambda l: l[0])  # 按y坐标排序

    # 合并相近的水平直线
    newlines = []
    merge_threshold = 10  # 合并阈值（像素）
    for y, x_start, x_end in splines:
        if not newlines:
            newlines.append([y, x_start, x_end])
        else:
            last_y, last_x_start, last_x_end = newlines[-1]
            # 如果两条线垂直距离小于阈值，则合并
            if abs(y - last_y) < merge_threshold:
                new_y = int((last_y + y) / 2)
                new_x_start = min(last_x_start, x_start)
                new_x_end = max(last_x_end, x_end)
                newlines[-1] = [new_y, new_x_start, new_x_end]
            else:
                newlines.append([y, x_start, x_end])

    # 可视化检测结果
    line_img = cv2.cvtColor(part_gray, cv2.COLOR_GRAY2BGR)
    for y, x_start, x_end in newlines:
        cv2.line(line_img, (x_start, y), (x_end, y), (0, 0, 255), 2)

    plt.figure(figsize=(12,6))
    plt.imshow(cv2.cvtColor(line_img, cv2.COLOR_BGR2RGB))
    plt.title(f"工件 {idx+1} 合并后的水平直线")
    plt.axis('off')
    plt.show()

    # 计算各水平线方程（形如y=?）
    ys = [line[0] for line in newlines]
    ys.sort()
    # 将检测到的水平线y坐标映射到特定编号
    keys = ["444", "445", "447", "448", "442", "443"]
    ys_dic = dict(zip(keys, ys))
    # 计算特定水平线之间的距离（像素单位）
    d_tu = [ys_dic["443"]-ys_dic["442"],
            ys_dic["448"]-ys_dic["445"],
            ys_dic["445"]-ys_dic["444"],
            ys_dic["448"]-ys_dic["447"],]
    # 将像素距离转换为实际物理距离（比例为0.025）
    d_shiji = [round(d*0.025,2) for d in d_tu]
    print(f"工件 {idx+1} 的水平线数量（已合并）:", len(newlines))
    print(f"工件 {idx+1} 水平线的y坐标:", ys)
    print(f"工件 {idx+1} 相邻水平线的距离:",
          "\n442-443:",d_shiji[0],"\n445-448:",d_shiji[1],
          "\n444-445:",d_shiji[2],"\n447-448:",d_shiji[3])
    print("——" * 20)

# ---------------------- 4. 主程序流程 ----------------------
if __name__ == "__main__":
    # 1. 图像读取与预处理
    gray, original, binary = preprocess()

    # 2. 工件分割与可视化
    parts = segment_parts(gray, original, binary)

    # 3. 循环处理每个工件
    for idx, part in enumerate(parts):
        process_single_part(part, idx)
