%%

nsteps = 8;
x_step_min = 0.2;
x_step_max = 1;
y_sigma = 0.025;

y = 0;
x = 0;
pts = [x, y];
sgn = ternary( rand < 0.5, -1, 1 );

for i = 0:nsteps-1
  y = min( 1, max(y, y + 1/nsteps + randn * y_sigma) );
  x = x + sgn * (rand * (x_step_max - x_step_min) + x_step_min);
  sgn = sgn * -1;
  pts(end+1, :) = [x, y];
end

pts(2:end, 2) = pts(2:end, 2) + max( 0, 1 - pts(end, 2) );

figure(1);
clf;
scatter( pts(:, 1), pts(:, 2) );
hold on;
plot( pts(:, 1), pts(:, 2) );
ylim( [0, 1] );
xlim( [-1, 1] );