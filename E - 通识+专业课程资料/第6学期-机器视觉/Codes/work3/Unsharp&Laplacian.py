import numpy as np
from PIL import Image

def gaussian_kernel(size=5, sigma=1.0):
    """生成高斯核"""
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= kernel.sum()  # 归一化
    return kernel

def convolve2d(image, kernel):
    """手动实现二维卷积（支持单通道）"""
    k_size = kernel.shape[0]
    pad = k_size // 2
    # 边界反射填充
    image_padded = np.pad(image, pad, mode='reflect')
    output = np.zeros_like(image)
    # 滑动窗口计算卷积
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = image_padded[i:i+k_size, j:j+k_size]
            output[i, j] = np.sum(region * kernel)
    return output

def unsharp_masking(image_array, sigma=1.0, strength=0.7):
    """反锐化掩模"""
    kernel = gaussian_kernel(sigma=sigma)
    blurred = np.zeros_like(image_array)
    # 对每个通道分别处理
    for c in range(3):
        blurred[:, :, c] = convolve2d(image_array[:, :, c], kernel)
    mask = image_array - blurred
    sharpened = image_array + strength * mask
    return np.clip(sharpened, 0, 1)

def laplacian_sharpen(image_array, strength=0.3):
    """拉普拉斯锐化"""
    kernel = np.array([[0, -1, 0],
                      [-1, 4, -1],
                      [0, -1, 0]], dtype=np.float32)
    sharpened = np.zeros_like(image_array)
    for c in range(3):
        edges = convolve2d(image_array[:, :, c], kernel)
        sharpened[:, :, c] = image_array[:, :, c] + strength * edges
    return np.clip(sharpened, 0, 1)

if __name__ == "__main__":
    # 读取图像并归一化
    img = Image.open("3-1.jpg")
    img_array = np.array(img, dtype=np.float32) / 255.0

    # 方法1：反锐化掩模（参数可调）
    sharpened_unsharp = unsharp_masking(img_array, sigma=1.5, strength=1.0)
    Image.fromarray((sharpened_unsharp * 255).astype(np.uint8)).save("sharpened_unsharp.jpg")

    # 方法2：拉普拉斯锐化（参数可调）
    sharpened_laplacian = laplacian_sharpen(img_array, strength=0.3)
    Image.fromarray((sharpened_laplacian * 255).astype(np.uint8)).save("sharpened_laplacian.jpg")