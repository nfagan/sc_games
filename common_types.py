from dataclasses import dataclass
from typing import List, Optional

@dataclass
class KeyEvent(object):
  timestamp: float
  keys: List[str]

@dataclass
class MovementHistoryRecord(object):
  timestamp: float
  point: List[float]
  movement: List[int]

@dataclass
class InteractStateResult(object):
  entered_timestamp: float
  exited_timestamp: float
  implement_movements: List[MovementHistoryRecord]
  implement_hit_collider: bool
  implement_hit_timestamp: Optional[float]
  collider_did_reach_target: bool
  collider_hit_timestamp: Optional[float]

@dataclass
class StaticStateResult(object):
  entered_timestamp: float
  exited_timestamp: float

@dataclass
class TrialRecord(object):
  present_background: Optional[StaticStateResult]
  interact: Optional[InteractStateResult]
  iti: Optional[StaticStateResult]

@dataclass
class TaskData(object):
  trials: List[TrialRecord]
  events: List[KeyEvent]

@dataclass
class YokeRecord(object):
  implement_hit: bool
  timestamp: float