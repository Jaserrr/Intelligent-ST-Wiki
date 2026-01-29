import numpy as np
from PIL import Image

img = Image.open('./work2-3/fig1.jpg').convert('L')
img_array = np.array(img)

# 计算直方图
hist, bins = np.histogram(img, 256, [0,256])

# 计算累积分布函数 (CDF)
cdf = hist.cumsum()
cdf_normalized = cdf * hist.max() / cdf.max()

# 使用累积分布函数作为变换函数进行直方图均衡化
cdf_m = np.ma.masked_equal(cdf,0)
cdf_m = (cdf_m - cdf_m.min())*255/(cdf_m.max()-cdf_m.min())
cdf = np.ma.filled(cdf_m,0).astype('uint8')

img2 = cdf[img]

Image.fromarray(img2).save('fig1_new.jpg')