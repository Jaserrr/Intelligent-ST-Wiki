close all;clear;clc; %复位MATLAB工作环境
xn=[1,1,1,1];        %x(n)序列值
subplot(2,1,1);
stem(xn);            %绘制x(n)波形图
N=1024;              %变换区间长度N取1024
XK=fft(xn,N);        %模拟DTFT变换
subplot(2,1,2);
plot(abs(XK));       %绘制X(K)幅度特性曲线