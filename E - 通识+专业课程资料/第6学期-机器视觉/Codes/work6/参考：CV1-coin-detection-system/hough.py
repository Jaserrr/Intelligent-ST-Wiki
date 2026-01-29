import cv2
import numpy as np
from scipy.ndimage import maximum_filter
from canny import canny_edge_detection

def hough_gradient(edges, rho_max=150):
    '''霍夫变换'''
    # 计算图像的梯度信息
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=5)
    gradient_direction = np.arctan2(sobely, sobelx)

    # 获取边缘点的坐标
    y_coords, x_coords = np.nonzero(edges)
    
    # 计算圆心坐标
    # 创建一个三维累加器数组，第三维用于梯度方向
    accumulator = np.zeros((rowsy, colx, rho_max), dtype=np.uint64)
    for y, x in zip(y_coords, x_coords):
        for r in range(1, rho_max):
            ry = np.sin(gradient_direction[y, x]) * r
            rx = np.cos(gradient_direction[y, x]) * r
            ry, rx = int(ry), int(rx)
            if 0 <= y + ry < rowsy and 0 <= x + rx < colx:
                accumulator[y + ry, x + rx, r] += 1

    return accumulator

def non_max_suppression(accumulator, filter_size):
    '''
    filter_size:: 定义滤波器大小
    '''

    local_max_z = maximum_filter(accumulator, size=filter_size, mode='constant')

    # 将每个维度上的非极大值置为 0
    local_max = (accumulator == local_max_z)

    # 将非极大值置为 0
    accumulator[~local_max] = 0
    return accumulator

def extract_circles(accumulator, rho_min, rho_max, rate=0.5):
    '''提取检测到的圆'''
    circles = []
    max_value = np.max(accumulator)
    for y in range(rowsy):
        for x in range(colx):
            for r_idx, acc_value in enumerate(accumulator[y, x, rho_min:rho_max]):
                if acc_value > int(rate * max_value):  # 使用param2_accumulator作为投票阈值
                    circles.append((x, y, r_idx + rho_min))
    return circles

def draw_circles(image, circles, thickness=5):
    # 绘制检测到的圆
    for (x, y, r) in circles:
        cv2.circle(image, (x, y), r, (0, 255, 0), thickness)

    # 显示结果
    cv2.imshow('Detected Circles', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 加载图像
image = cv2.imread('1.png')
rowsy, colx, _ = image.shape
# 图像预处理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 边缘检测
edges = canny_edge_detection(blurred, 50, 100)
accumulator = hough_gradient(edges, rho_max=150)
accumulator = non_max_suppression(accumulator, filter_size = (50, 50, 50))
circles = extract_circles(accumulator, rho_min=100, rho_max=150, rate=0.5)
draw_circles(image, circles, 5)