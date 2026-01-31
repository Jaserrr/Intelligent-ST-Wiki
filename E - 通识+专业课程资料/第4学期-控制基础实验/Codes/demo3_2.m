K = 10;
num = [K];  % 分子：K=10
den = [1, 6, 5, 0];  % 分母展开：s(s+1)(s+5) = s³+6s²+5s

% 1. 绘制Bode图并计算稳定裕度
figure(1);
bode(num, den);
title('K=10时的Bode图');
grid on;

[Gm, Pm, Wcg, Wcp] = margin(num, den);

% 2. 显示结果
disp('幅值裕度Gm：'); disp(Gm);
disp('相位裕度Pm（度）：'); disp(Pm);
disp('相位穿越频率Wcg（rad/s）：'); disp(Wcg);
disp('开环截止频率Wcp（rad/s）：'); disp(Wcp);

% 3. 判断稳定性
if Pm > 0 && Gm > 1
    disp('稳定裕度均为正值，系统稳定');  % 
else
    disp('系统不稳定');
end