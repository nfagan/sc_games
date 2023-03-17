from psychopy import event
import time
from typing import List
from dataclasses import dataclass

@dataclass
class KeyEvent(object):
  timestamp: float
  keys: List[str]

class TaskLoopResult(object):
  def __init__(self, keys, dt):
    self.keys = keys
    self.dt = dt

class Task(object):
  def __init__(self, window, abort_crit):
    self.window = window
    self.state_t0 = 0
    self.task_t0 = time.time()
    self.last_t = 0
    self.abort_crit = abort_crit
    self.pending_abort = False
    self.key_events = []

  def get_key_events(self):
    return self.key_events[:]

  def enter_state(self):
    self.state_t0 = time.time()
    self.last_t = self.state_t0

  def state_time(self):
    return time.time() - self.state_t0
  
  def task_time(self):
    return time.time() - self.task_t0

  def loop(self):
    curr_t = time.time()
    dt = curr_t - self.last_t
    self.last_t = curr_t

    self.window.flip()
    
    keys = event.getKeys()
    event.clearEvents()
    loop_res = TaskLoopResult(keys, dt)

    if len(keys) > 0:
      self.key_events.append(KeyEvent(self.task_time(), keys[:]))

    if self.abort_crit(loop_res):
      self.pending_abort = True

    return loop_res