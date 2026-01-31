% a) 生成 5 行、10 列的二维随机数组 A
A = round(rand(5, 10),2);
disp('原始数组 A：');
disp(A);

% b) 找出数组 A 中所有大于 0.48 且小于 0.52 的元素的单下标
place = find(A > 0.48 & A < 0.52);
disp('满足大于 0.48 且小于 0.52 条件的元素单下标：');
disp(place);

% c) 求出满足条件的元素的和与平均值，并保留两位小数
sum_val = round(sum(A(place)), 2);
mean_val = round(mean(A(place)), 2);
disp(['满足条件元素的和：', num2str(sum_val)]);
disp(['满足条件元素的平均值：', num2str(mean_val)]);