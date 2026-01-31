% 定义实验样本数据
x = [0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1];
y = [-0.232 0.647 1.877 3.565 5.134 7.443 9.221 10.011 11.678 12.566 13.788];

% 二次多项式拟合
p2 = polyfit(x, y, 2);
y2 = polyval(p2, x);

% 三次多项式拟合
p3 = polyfit(x, y, 3);
y3 = polyval(p3, x);

% 绘制原始数据和拟合曲线
figure;
plot(x, y, 'ro', 'MarkerSize', 8, 'DisplayName', '原始数据');
hold on;
plot(x, y2, 'b-', 'LineWidth', 2, 'DisplayName', '二次拟合');
plot(x, y3, 'g-', 'LineWidth', 2, 'DisplayName', '三次拟合');

% 添加图例、标题和坐标轴标签
legend('Location', 'best');
title('多项式拟合效果对比');
xlabel('x');
ylabel('y');
grid on;

% 输出拟合多项式系数
fprintf('二次拟合多项式: %.4fx^2 + %.4fx + %.4f\n', p2(1), p2(2), p2(3));
fprintf('三次拟合多项式: %.4fx^3 + %.4fx^2 + %.4fx + %.4f\n', p3(1), p3(2), p3(3), p3(4));    