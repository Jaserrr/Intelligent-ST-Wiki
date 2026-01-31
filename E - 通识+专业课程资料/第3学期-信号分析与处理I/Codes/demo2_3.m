close all;clear;clc; %复位MATLAB工作环境
syms z;
n=0:4;
f=ones(1,length(n)); %x(n)信号序列
Fz=sum(f.*z.^(-n)); %按定义计算 Z 变换
disp(Fz);
% 将Z变换表达式转为传递函数
[num,den]=numden(Fz); % 提取分子 (numerator) 和分母 (denominator)
num=double(coeffs(num,z,'All')); % 提取分子多项式的系数，并转为数值
den=double(coeffs(den,z,'All')); % 提取分母多项式的系数，并转为数值
sys=tf(num,den); % 使用分子和分母系数创建传递函数对象
% 绘制零极点图
figure;
zplane(num,den); % 绘制系统的零极点图
title('零极点图');
grid on;