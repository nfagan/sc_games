import numpy as np

def gen_trajectory(*, nsteps, x_step_min, x_step_max, y_sigma):
  y = 0.
  # x = (np.random.rand() * 2. - 1.)
  x = -0.75
  pts = [[x, y]]
  sgn = -1. if np.random.rand() < 0.5 else 1.

  for i in range(nsteps):
    y = min(1., max(y, y + 1./nsteps + np.random.randn() * y_sigma))
    x = x + sgn * (np.random.rand() * (x_step_max - x_step_min) + x_step_min)
    sgn = sgn * -1.
    pts.append([x, y])

  err = max(0., 1. - pts[-1][1])
  for i in range(nsteps-1):
    pts[i + 1][1] += err

  for i in range(nsteps):
    pts[i][1] = pts[i][1] * 2. - 1.

  return pts