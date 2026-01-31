close all;clear;clc;
omega1 = 2;  % 3dB截止频率 (rad/s)
omega2 = 6;  % 30dB截止频率 (rad/s)
% 计算滤波器的阶数和截止频率
[N, Wn] = cheb1ord(omega1, omega2, 3, 30, 's'); 
fprintf('阶数 N: %d\n', N);
% 计算滤波器传递函数
[b, a] = cheby1(N, 3, Wn, 's');
H = tf(b, a);
disp(H);
w = linspace(0, 5, 1000); 
Hfreq = freqs(b, a, w);
abshf = abs(Hfreq);
gyhf = abshf / max(abshf);% 将幅度归一化
figure;
plot(w, gyhf);  % 绘制归一化后的幅度
grid on;
title('I型切比雪夫低通滤波器幅频特性');
xlabel('频率 (rad/s)');
ylabel('幅度');
axis([0 5 0 1]);