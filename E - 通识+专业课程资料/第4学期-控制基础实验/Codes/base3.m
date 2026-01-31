x = linspace(0, 4*pi, 1000); % 生成[0,4π]范围内1000个点
y_sin = sin(x);
y_cos = cos(x);

figure;  % 创建图形
plot(x, y_sin, 'DisplayName', 'y=sin(x)');
hold on; % 保持，再画一条
plot(x, y_cos, 'bo', 'DisplayName', 'y=cos(x)'); % 蓝色小圆圈表示

% 添加标注、标题和图例
title('正弦余弦函数图像');
xlabel('x');
ylabel('y');
legend('Location','best');
grid on;

% 标注关键点
text(pi/2, 1, 'y=sin(x)', 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');
text(0, 1, 'y=cos(x)', 'HorizontalAlignment', 'center', 'VerticalAlignment', 'bottom');