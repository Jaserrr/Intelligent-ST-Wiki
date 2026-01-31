close all;clear;clc; %复位matlab工作环境
% 定义符号变量
syms t s
% 定义单位阶跃函数 u(t)
u=heaviside(t);
% 定义信号 x(t)
x=exp(-2*t)*u+exp(-3*t)*u;
% 计算拉普拉斯变换 X(s)
X_s=laplace(x,t,s);
disp('拉普拉斯变换 X(s):');
disp(X_s);
% 绘制 x(t) 在 t=0 到 t=5 之间的图像
fplot(x,[0 5]);
title('信号 x(t)');
xlabel('时间 t');
ylabel('幅度');
grid on;

% 将拉普拉斯变换表达式转为传递函数
[num,den]=numden(X_s); % 提取分子 (numerator) 和分母 (denominator)
num=double(coeffs(num,'All')); % 提取分子多项式的系数，并转为数值
den=double(coeffs(den,'All')); % 提取分母多项式的系数，并转为数值
sys=tf(num,den); % 使用分子和分母系数创建传递函数对象

% 绘制零极点图
figure;
pzmap(sys); % 绘制系统的零极点图
title('零极点图');
grid on;