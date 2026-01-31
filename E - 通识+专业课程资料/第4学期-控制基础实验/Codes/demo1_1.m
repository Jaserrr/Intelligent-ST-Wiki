num=[0 0 4];
t=0:0.1:10;
den1=[1 0 4];
den2=[1 2 4];
den3=[1 4 4];

hold on
step(num,den1,t);
step(num,den2,t);
step(num,den3,t);
grid
title('G(s)的单位阶跃响应曲线图');
legend('\zeta = 0', '\zeta = 0.5', '\zeta = 1.0'); 
hold off