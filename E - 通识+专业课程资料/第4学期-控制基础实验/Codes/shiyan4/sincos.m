x = linspace(0, 2*pi, 100);
y1 = sin(x); y2 = cos(x);

subplot(1,2,1)
scatter(x, y1, 20, 'r', 'Marker','o'), hold on
plot(x, y1, 'b-'), title('sin(x)'), grid on

subplot(1,2,2)
scatter(x, y2, 20, 'b', 'Marker','*'), hold on
plot(x, y2, 'b-'), title('cos(x)'), grid on