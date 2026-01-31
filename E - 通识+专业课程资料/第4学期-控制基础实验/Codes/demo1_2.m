num1=[0 0 1];
num2=[0 0 9];
num3=[0 0 36];
den1=[1 0.5 1];
den2=[1 1.5 9];
den3=[1 3.0 36];
hold on
t=0:0.1:10;
step(num1,den1,t);
step(num2,den2,t);
step(num3,den3,t);
grid
title('G(s)的单位阶跃响应曲线图')
legend('\omega_n = 1', '\omega_n = 3', '\omega_n = 6'); 
hold off