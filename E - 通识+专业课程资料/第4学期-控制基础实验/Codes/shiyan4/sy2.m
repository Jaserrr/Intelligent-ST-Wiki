x = [15.14,14.81,15.11,15.26,15.08,15.17,15.12,14.95,15.05,14.87];
[mu_hat, sigma_hat, mu_ci, sigma_ci] = normfit(x, 0.1); % 参数估计（0.1对应90%置信水平）

fprintf('总体均值估计值: %.4f\n', mu_hat);
fprintf('总体均值90%%置信区间: [%.4f, %.4f]\n', mu_ci(1), mu_ci(2));
fprintf('总体标准差估计值: %.4f\n', sigma_hat);
fprintf('总体标准差90%%置信区间: [%.4f, %.4f]\n', sigma_ci(1), sigma_ci(2));