T = readtable('体测成绩.xls');

% 身高分组统计
T1 = T(:, {'class', 'height'});  % 提取班级和身高列
tjl = {'mean', 'std', 'min', 'max'};  % 指定统计量
Tongji = grpstats(T1, 'class', tjl);   % 分组统计
Tongji.class = arrayfun(@(x) sprintf('%06d', x), Tongji.class, 'UniformOutput', false); % 修复class（转字符串）
disp('=== 各班级身高统计量 ===');
disp(Tongji);

% 计算相关系数矩阵
vars = {'height', 'weight', 'VC', 'score1', 'score2', 'score3'}; 
X = T(:, vars);                  % 提取目标列
X_data = table2array(X);         % 转换为数值矩阵
corr_matrix = corrcoef(X_data);  % 计算相关系数
corr_table = array2table(corr_matrix, ...
    'RowNames', vars, ...
    'VariableNames', vars);      % 转换为带变量名的表格
disp('=== 相关系数矩阵 ===');
disp(corr_table);