close all;clear;clc;
Omega_p = 0.5 * pi;  % 3dB截止频率 (rad)
Omega_s = 0.75 * pi; % 15dB截止频率 (rad)
T = 1;  % 采样周期 (s)
% 计算滤波器的阶数和截止频率
[N, Wn] = buttord(Omega_p / pi, Omega_s / pi, 3, 15); % 归一化
fprintf('阶数 N: %d\n', N);
% 计算数字滤波器传递函数
[b, a] = butter(N, Wn);
Hz = tf(b, a, T); % 数字系统函数
disp(Hz);
% 画幅频特性
figure;
[Hfreq, W] = freqz(b, a, 1024);
plot(W/pi, 20*log10(abs(Hfreq)));
grid on;
title('巴特沃斯低通数字滤波器 幅频特性');
xlabel('归一化频率 (×π rad/sample)');
ylabel('幅度 (dB)');
axis([0 1 -40 5]);
