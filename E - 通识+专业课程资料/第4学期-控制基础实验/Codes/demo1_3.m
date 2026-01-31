coeff = [2 1 3 5 10]; % 定义特征方程的系数向量
x = roots(coeff); % 求根
for i = 1:length(x)
    fprintf('根 %d: %.4f + %.4fi\n', i, real(x(i)), imag(x(i)));
end

if all(real(x) < 0) disp('系统稳定，所有根的实部均小于0');
else disp('系统不稳定，存在实部大于等于0的根');
end