close all;clear;clc; %复位matlab工作环境
tspan=0.01;          %设置信号的采样间隔
t1=-4:tspan:4;       %f1信号时间向量t1，取[-4,4]s
t1len=length(t1);    %t1的长度
t2=-4:tspan:4;       %f2信号时间向量t2，取[-4,4]s
t2len=length(t2);    %t2的长度
t3=-8:tspan:8;       %f3信号时间向量t3，取[-8,8]s
f1=[zeros(1,length(-4:tspan:(-2-0.01))),2*ones(1,length(-2:tspan:2)),zeros(1,length(2.01:tspan:4))];
%zeros函数创建全0矩阵，ones函数创建全1矩阵。
%生成f1信号，其中时间[-2,2]s的幅值为2，其他为0
f2=[zeros(1,length(-4:tspan:(0-0.01))),3/4*ones(1,length(0:tspan:2)),zeros(1,length(2.01:tspan:4))];
%生成f2信号，其中时间[0,2]s的幅值为3/4，其他为0
w=conv(f1,f2);       %对f1和f2采样数组向量进行卷积
w=w*tspan;           %乘以时间间隔
subplot(3,1,1);      %将当前图形划分为3*1网格，并选择区域1创建坐标轴
plot(t1,f1);         %绘制f1波形
title('f1信号波形');  %设置标题
grid on;             %显示网格
xlabel('时间t/s');   %设置横轴显示标签
ylabel('x_1(t)');    %设置纵轴显示标签
axis([-4 4 -2 2]);   %设置坐标范围
subplot(3,1,2);      %选择区域2创建坐标轴（与上方图形在一个图内）
plot(t2,f2);         %以下代码注释同上，不再赘述
title('f2信号波形');
grid on;
xlabel('时间t/s');
ylabel('x_2(t)');
axis([-4 4 -2 2]);
subplot(3,1,3);
plot(t3,w);
title('f1和f2信号卷积结果');
xlabel('时间t/s');
ylabel('y(t)');
grid on;