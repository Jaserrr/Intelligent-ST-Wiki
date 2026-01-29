import numpy as np
from PIL import Image

sum = None
for i in range(1,21):
    img = Image.open(f"./Frame Average/image_noise{i}.jpg")
    img_array = np.array(img, dtype=np.float32)
    if sum is None:
        # 创建全零数组，和输入数组形状、数据类型相同
        sum = np.zeros_like(img_array, dtype=np.float32)
    sum += img_array
aver_image = np.clip(sum/20,0,255).astype(np.uint8)
Image.fromarray(aver_image).save("output.jpg")