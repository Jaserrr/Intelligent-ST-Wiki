import cv2
import numpy as np

def canny_edge_detection(blurred, low_threshold=30, high_threshold=150):
    '''
    blurred:: 高斯模糊后的图像
    low_threshold:: 低阈值
    parameter:: 高阈值
    '''
    # 计算梯度
    grad_m, grad_d = compute_gradients(blurred)

    # 非极大值抑制
    suppressed = non_max_suppression(grad_m, grad_d)

    # 双阈值检测
    edges = thresholding(suppressed, low_threshold, high_threshold)

    return edges

def compute_gradients(image):
    # 计算水平方向上的梯度
    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)

    # 计算垂直方向上的梯度
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

    # 计算梯度幅值和梯度方向
    grad_m = np.sqrt(sobel_x**2 + sobel_y**2)
    grad_d = np.arctan2(sobel_y, sobel_x)

    return grad_m, grad_d

def non_max_suppression(grad_m, grad_d):
    # 将梯度方向转换为角度（弧度制）
    angle = grad_d * np.pi / 180.0
    
    # 获取图像尺寸
    height, width = grad_m.shape
    
    # 创建一个全零矩阵，用于存储非极大值抑制后的结果
    suppressed_edges = np.zeros_like(grad_m)
    
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # 获取当前像素点的梯度幅值
            mag = grad_m[y, x]
            
            # 获取当前像素点的梯度方向角度
            angle_val = angle[y, x]
            
            # 计算当前像素点相邻两个像素点的坐标
            x1 = int(np.round(x + np.cos(angle_val)))
            y1 = int(np.round(y + np.sin(angle_val)))
            x2 = int(np.round(x - np.cos(angle_val)))
            y2 = int(np.round(y - np.sin(angle_val)))
            
            # 判断当前像素点的梯度幅值是否为局部最大值
            if (mag >= grad_m[y1, x1]) and (mag >= grad_m[y2, x2]):
                suppressed_edges[y, x] = mag
    
    return suppressed_edges



def thresholding(image, low_threshold, high_threshold):
    # 创建一个全零矩阵，与输入图像大小相同，用于存储阈值处理后的结果
    thresholded_image = np.zeros_like(image)
    
    # 将低阈值和高阈值之间的像素设置为强边缘（255）
    strong_edges = (image >= high_threshold)
    
    # 将低阈值以下的像素设置为弱边缘（50）
    weak_edges = (image >= low_threshold) & (image < high_threshold)
    
    # 将强边缘和弱边缘合并到输出图像中
    thresholded_image[strong_edges] = 255
    thresholded_image[weak_edges] = 50
    
    return thresholded_image

def detect_coins(image_path):
    # 读取输入图像
    image = cv2.imread(image_path)

    # 将图像转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print(gray)

    # 对灰度图进行高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # print(blurred)

    # 进行Canny边缘检测
    # edges = cv2.Canny(blurred, 30, 150)
    edges = canny_edge_detection(blurred, 80, 100)

    # 显示结果图像
    cv2.imshow("Coins", edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if '__main__' == __name__:
    # 测试
    image_path = "1.png"
    detect_coins(image_path)