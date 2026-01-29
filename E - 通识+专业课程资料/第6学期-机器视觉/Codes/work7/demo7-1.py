import cv2

img = cv2.imread('blb1.jpg', cv2.IMREAD_GRAYSCALE)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))

img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

cv2.imwrite('blb1_open.jpg', img_open)
cv2.imwrite('blb1_close.jpg', img_close)

cv2.waitKey(0)
cv2.destroyAllWindows()
