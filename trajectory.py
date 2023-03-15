import numpy as np

def uniform_in_range(x0, x1):
  return x0 + (np.random.rand() * (x1 - x0))

def random_sign():
  return float(np.random.choice(2) * 2 - 1)

def extra_hard():
  x0 = uniform_in_range(0.75, 0.85) * random_sign()
  return gen_trajectory(x0=x0, nsteps=5, x_step_min=0.1, x_step_max=0.5, y_sigma=0.1)

def hard():
  x0 = uniform_in_range(0.6, 0.7) * random_sign()
  return gen_trajectory(x0=x0, nsteps=5, x_step_min=0.1, x_step_max=0.5, y_sigma=0.05)
  # return gen_trajectory(x0=x0, nsteps=6, x_step_min=0.2, x_step_max=0.3, y_sigma=0.05)

def med():
  x0 = uniform_in_range(0.35, 0.45) * random_sign()
  return gen_trajectory(x0=x0, nsteps=3, x_step_min=0.2, x_step_max=0.4, y_sigma=0.025)

def easy():  
  x0 = uniform_in_range(0.2, 0.25) * random_sign()
  return gen_trajectory(x0=x0, nsteps=2, x_step_min=0.2, x_step_max=0.4, y_sigma=0.025)

def gen_trajectory(**kwargs):
  while True:
    kps = gen_trajectory_(**kwargs)
    accept = all(map(lambda kp: kp[0] >= -1. and kp[0] <= 1. and kp[1] >= -1. and kp[1] <= 1., kps))
    if accept:
      return kps

def gen_trajectory_(*, nsteps, x0, x_step_min, x_step_max, y_sigma):
  assert x0 >= -1. and x0 <= 1.

  y = 0.
  x = float(x0)
  pts = [[x, y]]
  # sgn = -1. if np.random.rand() < 0.5 else 1.
  sgn = 1. if x0 >= 0 else -1

  for i in range(nsteps):
    y = min(1., max(y, y + 1./nsteps + np.random.randn() * y_sigma))
    x = x + sgn * uniform_in_range(x_step_min, x_step_max)
    sgn = sgn * -1.
    pts.append([x, y])

  err = max(0., 1. - pts[-1][1])
  for i in range(nsteps-1):
    pts[i + 1][1] += err

  for i in range(nsteps):
    pts[i][1] = pts[i][1] * 2. - 1.

  return pts