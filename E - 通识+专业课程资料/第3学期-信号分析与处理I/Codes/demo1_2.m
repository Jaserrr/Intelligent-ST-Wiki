close all;clear;clc;      % 复位matlab工作环境
syms t w                  % 定义符号变量 t 和 w
x=exp(-2*t)*heaviside(t); % 时间信号 x(t)
F=fourier(x,t,w);         % 傅里叶变换
% 绘制时间域信号 x(t)
subplot(3,1,1);           % 创建3×1子图，选中第1个区域
ezplot(x);                % 绘制时间域信号
xlabel('时间 t/s');       % 横轴标签
ylabel('x(t)');           % 纵轴标签
title('时间域信号x(t)');   % 标题
grid on;                  % 显示网格

% 绘制幅频特性 |X(w)|
subplot(3,1,2);                % 选中第2个区域
ezplot(abs(F));                % 绘制幅频特性 |X(w)|
xlabel('频率 \omega (rad/s)'); % 横轴标签
ylabel('|X(\omega)|');         % 纵轴标签
title('幅频特性 |X(\omega)|');  % 标题
grid on; % 显示网格

% 绘制相频特性 ∠X(w)
subplot(3,1,3);                % 选中第3个区域
ezplot(angle(F));              % 绘制相频特性 ∠X(w)
xlabel('频率 \omega (rad/s)'); % 横轴标签
ylabel('∠X(\omega)');         % 纵轴标签
title('相频特性 ∠X(\omega)');  % 标题
grid on;                       % 显示网格
