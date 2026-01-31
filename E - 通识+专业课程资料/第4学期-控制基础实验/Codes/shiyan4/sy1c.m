x = logspace(-1, 2);
y = exp(x);
loglog(x, y, 'b-');
xlabel('X');
ylabel('Y');
grid on;