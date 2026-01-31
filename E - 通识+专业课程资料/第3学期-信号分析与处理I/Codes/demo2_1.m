close all;clear;clc; %复位matlab工作环境
% 定义输入信号
x1=[1,1,1]; % R3(n)
x2=[1,2,3,4,5];
% 线性卷积
linear_conv=conv(x1,x2);
% 显示结果
disp('线性卷积结果:');
disp(linear_conv);

% 调用函数计算圆周卷积
cir_fft(x1,x2,8); % N=8
cir_fft(x1,x2,5); % N=5
function cir_fft(x1,x2,N)
    % 信号零填充到长度 N
    x1_pad=[x1,zeros(1,N-length(x1))];
    x2_pad=[x2,zeros(1,N-length(x2))];
    % 使用 FFT/IFFT 实现圆周卷积
    X1=fft(x1_pad); % x1 的 FFT
    X2=fft(x2_pad); % x2 的 FFT
    circular_conv_fft=ifft(X1.*X2); % 频域相乘，时域圆周卷积
    % 显示结果
    disp(['使用 FFT/IFFT 实现的圆周卷积结果（N=',num2str(N),'）:']);
    disp(real(circular_conv_fft));
end