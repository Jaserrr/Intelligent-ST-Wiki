import cv2
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def mean_filter(image, ksize):
    pad = ksize // 2
    padded = np.pad(image, pad, mode='edge')
    windows = sliding_window_view(padded, (ksize, ksize))
    return np.mean(windows, axis=(2, 3)).astype(image.dtype)

def median_filter(image, ksize):
    pad = ksize // 2
    padded = np.pad(image, pad, mode='edge')
    windows = sliding_window_view(padded, (ksize, ksize))
    return np.median(windows, axis=(2, 3)).astype(image.dtype)

image = cv2.imread('2-2.jpg', cv2.IMREAD_GRAYSCALE)
mean_filtered = mean_filter(image, ksize=7)
median_filtered = median_filter(image, ksize=3)

cv2.imwrite('mean_filtered.jpg', mean_filtered)
cv2.imwrite('median_filtered.jpg', median_filtered)


