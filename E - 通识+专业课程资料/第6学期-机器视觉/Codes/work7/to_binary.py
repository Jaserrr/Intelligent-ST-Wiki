import cv2
img = cv2.imread('document.bmp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 132, 255, cv2.THRESH_BINARY)
cv2.imwrite('binary.bmp', binary)
