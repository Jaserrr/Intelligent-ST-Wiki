% 生成网格点
x = linspace(-2, 2, 50);  % x范围：[-2, 2]，50个点
y = linspace(-2, 2, 50);  % y范围：[-2, 2]，50个点
[X, Y] = meshgrid(x, y);  % 生成二维网格

% 计算函数值
Z = X.^2 + Y.^2;  % z = x² + y²
figure('Position', [100, 100, 1000, 450]);  % 设置窗口大小

% 绘制三维网格图
subplot(1, 2, 1);
mesh(X, Y, Z);
title('z = x² + y² 的三维网格图');
xlabel('X'); ylabel('Y'); zlabel('Z');
grid on;
colormap jet;  % 设置颜色映射
colorbar;      % 添加颜色条

% 绘制三维曲面图
subplot(1, 2, 2);
surf(X, Y, Z);
title('z = x² + y² 的三维曲面图');
xlabel('X'); ylabel('Y'); zlabel('Z');
grid on;
colormap jet;  % 设置颜色映射
colorbar;      % 添加颜色条
shading interp; % 平滑着色
lightangle(45, 30); % 添加光照
lighting gouraud; % 设置光照模式