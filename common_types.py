from dataclasses import dataclass
from typing import List, Optional

@dataclass
class MRI_TR(object):
  timestamp: float
  index: int

@dataclass
class KeyEvent(object):
  timestamp: float
  keys: List[str]

@dataclass
class MovementHistoryRecord(object):
  timestamp: float
  point: List[float]
  movement: List[int]
  target_point: List[float]

@dataclass
class InteractStateResult(object):
  entered_timestamp: float
  exited_timestamp: float
  aversive_sound_timestamp: float
  implement_movements: List[MovementHistoryRecord]
  implement_hit_collider: bool
  implement_hit_timestamp: Optional[float]
  collider_did_reach_target: bool
  collider_hit_timestamp: Optional[float]
  began_touching_target_timestamps: List[float]
  stopped_touching_target_timestamps: List[float]
  collider_zigged_timestamps: List[float]

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