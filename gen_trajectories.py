import trajectory
import json
import os
import numpy as np

if __name__ == '__main__':
  n = 30  # num trials

  trajs = [trajectory.easy, trajectory.med, trajectory.hard, trajectory.extra_hard]
  traj_names = ['easy', 'medium', 'hard', 'extra_hard']

  for i in range(len(traj_names)):
    points = [trajs[i](sign=1.) for _ in range(n // 2)]
    signs = [1.] * (n // 2)

    # mirror a random trajectory
    neg_order = np.random.permutation(n // 2)
    for j in range(n // 2):
      points.append([[x[0] * -1., x[1]] for x in points[neg_order[j]]])
      signs.append(-1.)

    # shuffle left vs right start
    ord = np.random.permutation(n)
    points = [points[x] for x in ord]
    signs = [signs[x] for x in ord]

    samples = {
      'points': points,
      'signs': signs, 
      'difficulties': [traj_names[i]] * n
    }
    
    to_str = json.dumps(samples)
    fpath = os.path.join(os.getcwd(), 'res/trajectories', '{}.txt'.format(traj_names[i]))
    with open(fpath, 'w') as f:
      f.write(to_str)