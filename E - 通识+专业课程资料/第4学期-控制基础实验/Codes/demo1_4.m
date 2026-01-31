syms EPS %定义符号
den=[2,1,3,5,10];
ra=routh(den,EPS);
disp(ra)