function main() % 主函数
    vec = [-1,0,2,3,-5,4];
    s = fun(vec);
    disp(['向量中大于0的元素之和为：', num2str(s)]);
end

function s = fun(vec) % 子函数：计算向量中大于0的元素之和
    s = sum(vec(vec>0));
end