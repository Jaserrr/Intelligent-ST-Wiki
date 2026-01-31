[x,y] = meshgrid(-2:0.1:2, -2:0.1:2);
z = x.^2 + y.^2;
mesh(x,y,z);
xlabel('x'); ylabel('y'); zlabel('z');
title('z = x^2 + y^2');
grid on;