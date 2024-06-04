from typing import List, Tuple
import math
import numpy as np

class TargetMovement(object):
  def __init__(self) -> None:
    pass

  def tick(self, dt, ft, pos, reached_target):
    raise NotImplementedError
  
  def initial_position(self):
    raise NotImplementedError
  
  def reset(self):
    pass

class FixedDirectionMovement(TargetMovement):
  def __init__(self, vel) -> None:
    super().__init__()
    self.vel = vel

  def tick(self, dt, ft, pos, reached_target):
    if reached_target:
      return [0, 0], False
    return [x * dt for x in self.vel], False
  
class KeypointMovement(TargetMovement):
  def __init__(self, kps: List[Tuple[float, float]], speed_scale=1.) -> None:
    super().__init__()
    self.points = kps
    self.t = 0
    self.speed = 2. * speed_scale
    self.last_p0 = 0

  def reset(self):
    self.last_p0 = 0

  def tick(self, dt, ft, pos, reached_target):
    if reached_target:
      return [0, 0], False

    # self.t = max(0., min(1., self.t + dt * self.speed))
    self.t = max(0., min(1., ft * self.speed))
    kp_ind = len(self.points) * self.t
    kp0 = min(len(self.points)-1, math.floor(kp_ind))
    kp1 = min(len(self.points)-1, kp0 + 1)
    kpt = kp_ind - kp0
    p0 = np.array(self.points[kp0])
    p1 = np.array(self.points[kp1])
    target_p = (p1 - p0) * kpt + p0
    vel = target_p - np.array(pos)

    is_new = kp0 != self.last_p0
    self.last_p0 = kp0

    return [v for v in vel], is_new
  
  def initial_position(self):
    assert len(self.points) > 0
    return self.points[0][:]

class ZigMovement(TargetMovement):
  def __init__(self, p0, vel, zigs) -> None:
    super().__init__()
    self.p0 = p0
    self.vel = vel
    self.zigs = zigs

  def initial_position(self):
    return self.p0[:]
  
  def tick(self, dt, ft, pos, reached_target):
    if reached_target:
      return [0, 0], False
    is_new = False
    if len(self.zigs) > 0:
      zig_line_position = self.zigs[0]
      # if within 6 pixels of zigzag line, x-speed reverses (+/- 6 means condition always triggers since max speed is 9)
      if abs(pos[0] - zig_line_position) < 6:
        self.vel = (-self.vel[0], self.vel[1])
        self.zigs.pop(0)
        is_new = True
    return self.vel[:], is_new