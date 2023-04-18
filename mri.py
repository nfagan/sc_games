from common_types import MRI_TR
from typing import List
import dataclasses

TR_KEY = '5'

class MRIInterface(object):
  def __init__(self, enabled) -> None:
    self.trs: List[MRI_TR] = []
    self.tr = 0
    self.has_new_tr = False
    self.enabled = enabled

  def listen_for_tr(self, keys, timestamp: float):
    if TR_KEY not in keys:
      return
    
    self.has_new_tr = True
    self.trs.append(MRI_TR(timestamp, self.tr))
    self.tr += 1

  def check_for_new_tr(self):
    if self.has_new_tr:
      self.has_new_tr = False
      return True
    return False
  
  def get_trs(self) -> List[MRI_TR]:
    return [*map(lambda rec: dataclasses.asdict(rec), self.trs)]

  def wait_for_new_tr(self, wait_cb, ts: float):
    if not self.enabled:
      return

    while True:
      if self.check_for_new_tr() and self.trs[-1].timestamp > ts:
        break
      wait_cb()
