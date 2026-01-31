close all;clear;clc; % 复位matlab工作环境
x_n=ones(1,4);       % 定义矩形信号 R4(n)
% 调用函数计算和绘制频谱
plot_dft(x_n,8);  % 计算并绘制8点DFT
plot_dft(x_n,16); % 计算并绘制16点DFT
function plot_dft(x_n, N)
    x_n_padded=[x_n,zeros(1,N-length(x_n))]; % 信号零填充
    X=fft(x_n_padded); % 计算 DFT
    k=0:N-1;% 频率索引
    % 绘制频谱
    figure;
    stem(k,abs(X),'filled');
    title(['DFT 幅度谱 |X(k)|,N=',num2str(N)]);
    xlabel('频率索引 k');
    ylabel('幅度|X(k)|');
    grid on;
end
