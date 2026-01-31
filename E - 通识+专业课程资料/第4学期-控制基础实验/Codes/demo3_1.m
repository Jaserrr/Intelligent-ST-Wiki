f1 = [1 0]; f2 = [1 2]; f3 = [2 1 5];
num = [10, 30];
den = conv(conv(f1,f2),f3);  % 分母

% 1. 绘制Nyquist图
figure(1);
w = logspace(-2, 3, 1000);  % 设定频率范围10^-2到10^3，100个点
nyquist(num, den, w);
title('Nyquist曲线');
grid on;
ylim([-20,20]);

% 2. 绘制Bode图
figure(2);
bode(num, den, w);
title('Bode图');
grid on;

% 3. 计算开环极点，判断右极点数P
[z, p, k] = tf2zp(num, den);
disp('开环极点：');
disp(p);

% 4. 计算稳定裕度（辅助判断稳定性）
[Gm, Pm, Wcg, Wcp] = margin(num, den);
disp('幅值裕度Gm：'); disp(Gm);
disp('相位裕度Pm（度）：'); disp(Pm);
disp('相位穿越频率Wcg：'); disp(Wcg);
disp('开环截止频率Wcp：'); disp(Wcp);
