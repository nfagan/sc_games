from common_types import KeyEvent
from mri import MRIInterface
from psychopy import event
import time

class TaskLoopResult(object):
  def __init__(self, keys, dt):
    self.keys = keys
    self.dt = dt

class Task(object):
  def __init__(self, *, window, abort_crit, mri_interface: MRIInterface):
    self.window = window
    self.state_t0 = 0
    self.task_t0 = time.time()
    self.last_t = 0
    self.abort_crit = abort_crit
    self.pending_abort = False
    self.key_events = []
    self.mri_interface = mri_interface

  def get_key_events(self):
    return self.key_events[:]

  def enter_state(self):
    self.state_t0 = time.time()
    self.last_t = self.state_t0

  def state_time(self):
    return time.time() - self.state_t0
  
  def task_time(self):
    return time.time() - self.task_t0
  
  def wait_for_mri_tr(self):
    self.mri_interface.wait_for_new_tr(lambda: self.loop())

  def get_mri_trs(self):
    return self.mri_interface.get_trs()

  def loop(self):
    curr_t = time.time()
    dt = curr_t - self.last_t
    self.last_t = curr_t

    self.window.flip()
    
    keys = event.getKeys()
    event.clearEvents()
    loop_res = TaskLoopResult(keys, dt)

    if len(keys) > 0:
      t = self.task_time()
      self.mri_interface.listen_for_tr(keys, t)
      self.key_events.append(KeyEvent(t, keys[:]))

    if self.abort_crit(loop_res):
      self.pending_abort = True

    return loop_res