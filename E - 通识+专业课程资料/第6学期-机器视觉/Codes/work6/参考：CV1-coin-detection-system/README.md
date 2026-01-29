# 硬币检测系统

## 项目简介
本项目是一个基于图像处理技术的硬币检测系统，能够自动识别和定位图像中的硬币。系统使用了Canny边缘检测算法和霍夫变换（Hough Transform）算法来实现硬币的边缘检测和形状识别。

## 主要功能
- **Canny边缘检测**：自动检测图像中硬币的边缘。
- **霍夫变换**：识别图像中的圆形对象，即硬币。
- **图像显示**：将检测结果以图形界面展示。

## 技术栈
- OpenCV：用于图像处理和显示。
- NumPy：提供强大的多维数组对象。
- SciPy：用于科学计算，本项目中用于非极大值抑制。

## 安装指南
1. 安装Python环境（推荐使用Python 3.6及以上版本）。
2. 使用pip安装所需库：
   ```bash
   pip install numpy opencv-python
   ```
3. 确保系统中已安装SciPy库。

## 使用方法
1. 将项目代码克隆到本地：
   ```bash
   git clone https://github.com/rascal-yang/CV1-coin-detection-system.git
   ```
2. 进入项目目录：
   ```bash
   cd coin-detection-system
   ```
3. 运行Canny边缘检测脚本：
   ```bash
   python canny.py
   ```
4. 运行霍夫变换检测脚本：
   ```bash
   python hough.py
   ```

## 文件说明
- `canny.py`：包含Canny边缘检测算法的实现。
- `hough.py`：包含霍夫变换圆形检测算法的实现。
- `coins.jpg`：示例图像，用于测试硬币检测功能。

## 项目结构
```
coin-detection-system/
│
├── canny.py      # Canny边缘检测实现
├── hough.py      # 霍夫变换实现
└── coins.jpg     # 测试图像
```

## 注意事项
- 确保测试图像`coins.jpg`与脚本位于同一目录下，或修改脚本中的图像路径为正确的文件路径。
- 根据实际图像内容调整Canny边缘检测和霍夫变换的参数，以获得最佳检测效果。