f1 = [1 0]; f2 = [1 2 2]; f3 = [1 6 13];
den = conv(conv(f1,f2),f3);
num = [1];           % 分子多项式系数（对应增益K）
sys = tf(num, den);  % 开环传递函数

% 绘制根轨迹并求稳定K范围
figure;
rlocus(sys);
grid on;
xlabel('实轴');
ylabel('虚轴');
title('系统G(s)的根轨迹');

% 获取临界稳定增益（在图中点击虚轴交点）
[k_critical, r] = rlocfind(sys);
fprintf('闭环系统稳定的K值范围：0 < K < %.4f\n', k_critical);

% 绘制K=1时的阶跃响应
K=1;
sys_open = K*sys;
sys_closed = feedback(sys_open,1);  % 单位负反馈
figure;
step(sys_closed);
grid on;
xlabel('时间（s）');
ylabel('幅值');
title(['K=1 时的阶跃响应']);