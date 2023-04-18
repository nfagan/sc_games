from common_types import YokeRecord, KeyEvent, TrialRecord, MRI_TR
import random
import os
import json
import numpy as np
import math
import pickle
from typing import List, Optional

balloon_Y_start = 0
balloon_Y_speed = 6
egg_Y_start = 0

balloon_trajectory_info = [
    (-675, balloon_Y_start, 6, balloon_Y_speed, [70, -145]),
    (-600, balloon_Y_start, 0, balloon_Y_speed, []),
    (-575, balloon_Y_start, 5, balloon_Y_speed, [-200, -500, 290]),
    (-575, balloon_Y_start, -2, balloon_Y_speed, [-600, -400]),
    (-400, balloon_Y_start, 8, balloon_Y_speed, [0, -360, 650, -500, 500]),
    (-400, balloon_Y_start, 6, balloon_Y_speed, []),
    (-400, balloon_Y_start, -7, balloon_Y_speed, [-575, 300]),
    (-360, balloon_Y_start, 9, balloon_Y_speed, [0, -300, -150]),
    (-360, balloon_Y_start, 6, balloon_Y_speed, [-75, -150, 150, -290]),
    (-360, balloon_Y_start, 3, balloon_Y_speed, [-75]),
    (-350, balloon_Y_start, -1, balloon_Y_speed, []),
    (-300, balloon_Y_start, 7, balloon_Y_speed, [576, 432]),
    (-275, balloon_Y_start, 7, balloon_Y_speed, [0, -575, -300]),
    (-350, balloon_Y_start, 8, balloon_Y_speed, [-200, -300]),
    (-225, balloon_Y_start, 7, balloon_Y_speed, [-144, -504, 216]),
    (-150, balloon_Y_start, 0, balloon_Y_speed, []),
    (425, balloon_Y_start, -3, balloon_Y_speed, [300]),
    (200, balloon_Y_start, -7, balloon_Y_speed, [50, 600]),
    (225, balloon_Y_start, -9, balloon_Y_speed, [0, 580, -215, 215, -500, 575]),
    (300, balloon_Y_start, -5, balloon_Y_speed, [100, 200, -100]),
    (300, balloon_Y_start, -9, balloon_Y_speed, [-575, 575, -575, 575]),
    (300, balloon_Y_start, 2, balloon_Y_speed, []),
    (360, balloon_Y_start, -5, balloon_Y_speed, [0, 430]),
    (360, balloon_Y_start, -5, balloon_Y_speed, [75]),
    (360, balloon_Y_start, 6, balloon_Y_speed, [510]),
    (450, balloon_Y_start, -9, balloon_Y_speed, [390, 505, 450, 600, 500, 600, 550, 625]),
    (400, balloon_Y_start, -6, balloon_Y_speed, [-580, -290, -325]),
    (400, balloon_Y_start, -6, balloon_Y_speed, [140]),
    (650, balloon_Y_start, -8, balloon_Y_speed, [250, 675]),
    (650, balloon_Y_start, 0, balloon_Y_speed, [])]

# # easy
# balloon_trajectory_info = [balloon_trajectory_info[-7]] * 10

# # easy-med
# balloon_trajectory_info = [balloon_trajectory_info[0]] * 10

# medium
# balloon_trajectory_info = [balloon_trajectory_info[2]] * 10

# # hard
# balloon_trajectory_info = [balloon_trajectory_info[-5]]
# for i in range(10):
#   traj = list(balloon_trajectory_info[0])
#   xoff = -250 * i
#   traj[0] += xoff
#   traj[4] = [x + xoff for x in traj[4]]
#   balloon_trajectory_info.append(tuple(traj))

egg_zigs = []
egg_trajectory_info = [
    (0, egg_Y_start, 0, -4, egg_zigs),
    (-360, egg_Y_start, 4, -4, egg_zigs),
    (575, egg_Y_start, -3, -4, egg_zigs),
    (-550, egg_Y_start, 4, -6, egg_zigs),
    (-360, egg_Y_start, 0, -4, egg_zigs),
    (650, egg_Y_start, -5, -4, egg_zigs),
    (10, egg_Y_start, 3, -4, egg_zigs),
    (-450, egg_Y_start, 7, -5, egg_zigs),
    (70, egg_Y_start, 3, -4, egg_zigs),
    (-100, egg_Y_start, -1, -6, egg_zigs),
    (510, egg_Y_start, -3, -6, egg_zigs),
    (420, egg_Y_start, -2, -5, egg_zigs),
    (-620, egg_Y_start, 0, -7, egg_zigs),
    (-500, egg_Y_start, 7, -6, egg_zigs),
    (170, egg_Y_start, -3, -5, egg_zigs),
    (-360, egg_Y_start, 4, -4, egg_zigs),
    (590, egg_Y_start, -3, -4, egg_zigs),
    (700, egg_Y_start, -7, -5, egg_zigs),
    (-650, egg_Y_start, 4, -4, egg_zigs),
    (-360, egg_Y_start, 0, -4, egg_zigs),
    (200, egg_Y_start, 0, -6, egg_zigs),
    (100, egg_Y_start, 3, -5, egg_zigs),
    (-375, egg_Y_start, 2, -7, egg_zigs),
    (0, egg_Y_start, 0, -4, egg_zigs),
    (75, egg_Y_start, 3, -4, egg_zigs),
    (-215, egg_Y_start, 4, -5, egg_zigs),
    (500, egg_Y_start, -3, -4, egg_zigs),
    (420, egg_Y_start, -5, -4, egg_zigs),
    (-575, egg_Y_start, 0, -4, egg_zigs),
    (600, egg_Y_start, 0, -7, egg_zigs)]

def balloon_zigs(tn):
  if tn < len(balloon_trajectory_info):
    return balloon_trajectory_info[tn][4][:]
  else:
    return []

def balloon_position(tn, screen_height):
  y = -screen_height * 0.5
  if tn < len(balloon_trajectory_info):
    return [balloon_trajectory_info[tn][0], y]
  else:
    return [0, y]

def balloon_velocity(tn):
  if tn < len(balloon_trajectory_info):
    return [balloon_trajectory_info[tn][2], balloon_trajectory_info[tn][3]]
  else:
    return [0, balloon_Y_speed]

def egg_zigs(tn):
  return []

def egg_position(tn, screen_height):
  y0 = int(0.85 * screen_height * 0.5)
  if tn < len(egg_trajectory_info):
    return [egg_trajectory_info[tn][0], y0]
  else:
    return [0, y0]

def egg_velocity(tn):
  if tn < len(egg_trajectory_info):
    return [egg_trajectory_info[tn][2], egg_trajectory_info[tn][3]]
  else:
    return [0, -1]
  
def load_trajectories(kind):
  assert kind in ['easy', 'medium', 'hard', 'extra_hard']
  data_p = os.path.join(os.getcwd(), 'res/trajectories', '{}.txt'.format(kind))
  with open(data_p, 'r') as f:
    s = f.read()
  return json.loads(s)

def decode_pickled_yoke_file(b: bytes) -> List[YokeRecord]:
  y = pickle.load(b)
  k = [*sorted([*y.keys()])]
  res = []
  for i in k:
    ts = y[i]
    if ts is None:
      res.append(YokeRecord(False, None))
    else:
      res.append(YokeRecord(True, ts))
  return res

def decode_json_yoke_file_source(s: str) -> List[YokeRecord]:
  y = json.loads(s)
  assert isinstance(y, list)
  res = []
  for entry in y:
    ts = entry['timestamp']
    ts = None if math.isnan(ts) else ts
    res.append(YokeRecord(entry['implement_hit'], ts))
  return res

def convert_original_data_structure_trial_records_to_str(rows):
  if len(rows) == 0:
    return ''
  lines = []
  lines.append('# Version: xxxx')
  lines.append('# Task type: xxxx')
  lines.append('# Task mode: xxxx')
  lines.append('# Trajectory order: xxxx')
  for i in range(len(rows)):
    row = rows[i]
    keys = row.keys()
    if i == 0:
      lines.append('\t'.join(keys))
    line = []
    for k in keys:
      line.append(str(row[k]))
    lines.append('\t'.join(line))
  return '\n'.join(lines)

def convert_json_trial_data_to_original_data_structure(y, str_convert):
  trials = y['trials']
  rows = []
  for ti in range(len(trials)):
    trial_rows = convert_trial_data_to_original_data_structure(
      trials[ti], ti, y['events'], y['participant_id'], 
      y['trajectories']['points'][ti], y['mri_trs'])
    rows.extend(trial_rows)

  if str_convert:
    return convert_original_data_structure_trial_records_to_str(rows)
  else:
    return rows

def convert_trial_data_to_original_data_structure(
  trial: TrialRecord, trial_num: int, events: List[KeyEvent], part_id: str,
  trajectory: List[List[float]], trs: List[MRI_TR]):
  # 
  traj_str = []
  for x in trajectory:
    y = '(' + ','.join([*map(str, x)]) + ')'
    traj_str.append(y)
  traj_str = ', '.join(traj_str)

  def empty_row():
    nan = float('nan')
    return {
      'Participant_ID': part_id,
      'trial_num': trial_num,
      'timestamp': nan,
      'time_of_day_in_seconds': nan,
      'time_in_trial': nan,
      'X_target': nan,
      'Y_target': nan,
      'X_implement': nan,
      'Y_implement': nan,
      'keyboard_used': 0,
      'keys_pressed': '',
      'implement_move_direction': '',
      'target_zigged': False,
      'target_frozen': False,
      'touching_target_object': False,
      'target_outside_catchable_area': False,
      'just_made_magic': False,
      'just_made_first_contact': False,
      'target_just_froze': False,
      'target_just_exited_catchable_area': False,
      'aversive_noise_onset': False,
      'antic_period_onset': False,
      'avoid_period_onset': False,
      'iti_onset': False,
      'trial_offset': 0,
      'trial_trajectory': traj_str,
      'last_tr_num': -1,
      'total_frames_dropped': 0
    }
  
  antic = trial['present_background']
  avoid = trial['interact']
  iti = trial['iti']
  trial_start = antic['entered_timestamp']
  trial_end = iti['exited_timestamp']

  def set_timestamp(row, timestamp):
    row['timestamp'] = timestamp
    row['time_of_day_in_seconds'] = timestamp
    row['time_in_trial'] = timestamp - trial_start

    tr = None
    for i in range(len(trs)):
      if timestamp >= trs[i]['timestamp']:
        tr = trs[i]['index']
    if tr is not None:
      row['last_tr_num'] = tr

  rows = []

  # movements
  for move in trial['interact']['implement_movements']:
    move_dir = move['movement']
    move_dir_s = 'NA'
    if move_dir[0] == 1 and move_dir[1] == 0:
      move_dir_s = 'right'
    elif move_dir[0] == -1 and move_dir[1] == 0:
      move_dir_s = 'left'
    elif move_dir[0] == 0 and move_dir[1] == 1:
      move_dir_s = 'up'
    elif move_dir[0] == 0 and move_dir[1] == -1:
      move_dir_s = 'down'      

    row = empty_row()
    set_timestamp(row, move['timestamp'])

    row['X_target'] = move['target_point'][0]
    row['Y_target'] = move['target_point'][1]
    row['X_implement'] = move['point'][0]
    row['Y_implement'] = move['point'][1]
    row['implement_move_direction'] = move_dir_s
    rows.append(row)

  # key events
  key_events_this_trial = [*filter(
    lambda e: e['timestamp'] >= trial_start and e['timestamp'] < trial_end, events)]
  for evt in key_events_this_trial:
    row = empty_row()
    set_timestamp(row, evt['timestamp'])
    row['keyboard_used'] = 1
    row['keys_pressed'] = ','.join(evt['keys'])
    rows.append(row)

  # target zigged
  for ts in avoid['collider_zigged_timestamps']:
    row = empty_row()
    set_timestamp(row, ts)
    row['target_zigged'] = True
    rows.append(row)

  # target_frozen

  # touching_target_object
  for ts in avoid['began_touching_target_timestamps']:
    row = empty_row()
    set_timestamp(row, ts)
    row['touching_target_object'] = True
    rows.append(row)

  # target_outside_catchable_area

  # just_made_magic

  # just_made_first_contact
  if avoid['implement_hit_timestamp'] is not None:
    row = empty_row()
    set_timestamp(row, avoid['implement_hit_timestamp'])
    row['just_made_first_contact'] = True
    rows.append(row)

  # target_just_froze

  # target_just_exited_catchable_area
  if avoid['collider_hit_timestamp'] is not None:
    row = empty_row()
    set_timestamp(row, avoid['collider_hit_timestamp'])
    row['target_just_exited_catchable_area'] = True
    rows.append(row)
  
  # aversive_noise_onset
  if avoid['aversive_sound_timestamp'] is not None:
    row = empty_row()
    set_timestamp(row, avoid['aversive_sound_timestamp'])
    row['aversive_noise_onset'] = True
    rows.append(row)

  # antic_period_onset
  row = empty_row()
  set_timestamp(row, antic['entered_timestamp'])
  row['antic_period_onset'] = True
  rows.append(row)

  # avoid_period_onset
  row = empty_row()
  set_timestamp(row, avoid['entered_timestamp'])
  row['avoid_period_onset'] = True
  rows.append(row)

  # iti_onset
  row = empty_row()
  set_timestamp(row, iti['entered_timestamp'])
  row['iti_onset'] = True
  rows.append(row)

  # trial_offset
  row = empty_row()
  row['trial_offset'] = True
  set_timestamp(row, trial_end)
  rows.append(row)

  # result
  rows = [*sorted(rows, key=lambda x: x['timestamp'])]
  return rows