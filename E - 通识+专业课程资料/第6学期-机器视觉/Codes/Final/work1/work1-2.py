import cv2 as cv
import numpy as np

def line_detection(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # 转为灰度
    edges = cv.Canny(gray, 50, 150, apertureSize=3) # 求取边缘 窗口大小apertureSize=3
    lines = cv.HoughLines(edges, 1, np.pi/180, 150)# np.pi/180每次偏转1度
    for line in lines:
        print(line)
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0+1000*(-b))
        y1 = int(y0+1000*(a))
        x2 = int(x0-1000*(-b))
        y2 = int(y0-1000*(a))
        cv.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv.imwrite("image-lines.png", image)

src = cv.imread("14raw.bmp")
cv.namedWindow("input image", cv.WINDOW_AUTOSIZE)
line_detection(src)
