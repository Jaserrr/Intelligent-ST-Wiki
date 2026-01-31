close all;clear;clc;
fs = 1000;% 采样频率 (Hz)
t = 0:1/fs:5;% 时间向量
f = 400;% 信号频率 (Hz)
x = sin(2*pi*f*t);% 原始信号
noise = randn(size(t));% 白噪声
xa = x + noise;% 叠加噪声的信号
n = 500;
f=[0 396/500 398/500 402/500 404/500 1];
m=[0 0 1 1 0 0];
b = fir2(n, f, m); 
xf = filter(b, 1, xa); % 滤波后的信号
figure(1);
% 原始信号
subplot(3, 1, 1);
plot(t, x);
axis([1 1.3 -1 1]);
title('原始无噪声信号');
xlabel('时间 (s)');
ylabel('幅度');
grid on;
% 叠加噪声的信号
subplot(3, 1, 2);
plot(t, xa);
axis([1 1.3 -1 1]);
title('叠加了噪声的信号');
xlabel('时间 (s)');
ylabel('幅度');
grid on;
% 滤波后的信号
subplot(3, 1, 3);
plot(t, xf);
axis([1 1.3 -1 1]);
title('滤波后的信号');
xlabel('时间 (s)');
ylabel('幅度');
grid on;
% 绘制滤波器的幅频特性
figure(2);
[H, f] = freqz(b, 1, 1024, fs); % 计算频率响应
plot(f, 20*log10(abs(H))); % 幅度响应
title('FIR滤波器的幅频特性');
xlabel('频率 (Hz)');
ylabel('幅度 (dB)');
grid on;
ylim([-100 5]); 