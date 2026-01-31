close all;clear;clc;
w1 = 2;  % 3dB截止频率 (rad/s)
w2 = 6;  % 30dB截止频率 (rad/s)
[N, Wn] = buttord(w1, w2, 3, 30, 's'); % 计算滤波器的阶数和截止频率
fprintf('阶数 N: %d\n', N);
% 计算滤波器传递函数
[b, a] = butter(N, Wn, 's');
H = tf(b, a);
disp(H);
w = linspace(0, 5, 1000); % 定义频率范围向量w
Hfreq = freqs(b, a, w);
absHfreq = abs(Hfreq);
gyhf = absHfreq / max(absHfreq);% 将幅度归一化
% 画幅频特性
figure;
plot(w, gyhf);  % 绘制归一化后的幅度
grid on;
title('巴特沃斯低通滤波器幅频特性');
xlabel('频率 (rad/s)');
ylabel('幅度');
axis([0 5 0 1]);