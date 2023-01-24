from psychopy import event
import time

class TaskLoopResult(object):
  def __init__(self, keys, dt):
    self.keys = keys
    self.dt = dt

class Task(object):
  def __init__(self, window):
    self.window = window
    self.state_t0 = 0
    self.last_t = 0
    pass

  def enter_state(self):
    self.state_t0 = time.time()
    self.last_t = self.state_t0

  def state_time(self):
    return time.time() - self.state_t0

  def loop(self):
    curr_t = time.time()
    dt = curr_t - self.last_t
    self.last_t = curr_t

    self.window.flip()
    keys = event.getKeys()
    event.clearEvents()
    return TaskLoopResult(keys, dt)