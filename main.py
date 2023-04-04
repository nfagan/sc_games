from task import Task
from common_types import TaskData, TrialRecord
import states
import util
import data
import trajectory
from movement import ZigMovement, KeypointMovement
from psychopy import visual, core
import argparse
import os
from os import path
from typing import List
import dataclasses
from datetime import datetime
import json

DEBUG_NUM_TRIALS = 8
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
BORDER_WIDTH = 30 # pixels, width of yellow/purple border; approximate.
FULL_SCREEN = False
RES_ROOT = path.join(os.getcwd(), 'res')
KEY_MAP = {
  'move_left': '4',
  'move_right': '2',
  'move_down': '3',
  'move_up': '1',
  'stop': 'escape'
}
MOVE_INCR_PX = 80
TASK_TYPE = 'balloon'
CONTEXT = {'difficulty': '', 'trajectories': None}

def set_debug_keys():
  KEY_MAP['move_left'] = 'a'
  KEY_MAP['move_right'] = 'd'
  KEY_MAP['move_up'] = 'w'
  KEY_MAP['move_down'] = 's'

def res_path(p):
  return path.join(RES_ROOT, p)

def create_window():
  return visual.Window(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT), monitor = 'testMonitor', allowGUI=False, 
    fullscr=FULL_SCREEN, useFBO=False, units='pix')

def create_fullscreen_image_stim(win, p):
  return util.create_image_stim(win, p, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

def create_balloon_stimuli(win):
  string_suffix = '_no_string'
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Balloon_anticipatory_background.jpg')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Balloon_avoidance_background.jpg')),
    'collider_stim': util.create_image_stim(win, res_path('images/pink_balloon{}.png'.format(string_suffix))),
    'collided_stim': util.create_image_stim(win, res_path('images/pop_1{}.png'.format(string_suffix)))
  }

def create_egg_stimuli(win):
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Egg_anticipatory_background.jpg')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Egg_avoidance_background.jpg')),
    'collider_stim': util.create_image_stim(win, res_path('images/egg.png')),
    'collided_stim': util.create_image_stim(win, res_path('images/cracking_egg_1.png'))
  }

def create_iceberg_stimuli(win):
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Iceberg_anticipatory_background.png')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Iceberg_avoidance_background.png')),
    'collider_stim': util.create_image_stim(win, res_path('images/egg.png')),
    'collided_stim': util.create_image_stim(win, res_path('images/pop_1.png'))
  }

def gen_keypoints(trial, trajectories):
  if trajectories is not None:
    kps = trajectories['points'][trial][:]
  else:
    kp_fns = [trajectory.easy, trajectory.med, trajectory.hard, trajectory.extra_hard]
    kp_fn = kp_fns[trial % len(kp_fns)]
    kps = kp_fn()
  kps = [[x[0] * SCREEN_WIDTH * 0.5, x[1] * SCREEN_HEIGHT * 0.5] for x in kps]
  return kps

def make_balloon_movement_info(stimuli, trajectories):
  if True:
    get_movement = lambda tn: KeypointMovement(gen_keypoints(tn, trajectories))
  else:
    get_movement = lambda tn: ZigMovement(
      data.balloon_position(tn, SCREEN_HEIGHT), data.balloon_velocity(tn), data.balloon_zigs(tn))
  return {
    'get_movement': get_movement,
    'reached_target': lambda pos: pos[1] > SCREEN_HEIGHT * 0.5 - stimuli['collider_stim'].height * 0.5
  }

def make_egg_movement_info(stimuli):
  p0 = [0, SCREEN_HEIGHT * 0.5]
  return {
    'get_movement': lambda tn: ZigMovement(p0, data.egg_velocity(tn), data.egg_zigs(tn)),
    'reached_target': lambda pos: pos[1] < -SCREEN_HEIGHT * 0.5 + stimuli['collider_stim'].height * 0.5
  }

def make_iceberg_movement_info(stimuli):
  return make_egg_movement_info(stimuli)

def get_counter_stim_text_fn(trial):
  if CONTEXT['difficulty'] == 'debug':
    trial_difficulty = ['easy', 'medium', 'hard', 'extra-hard'][trial % 4]
    return lambda count: '({}) spells cast: {}'.format(trial_difficulty, count)
  else:
    return lambda count: 'spells cast: {}'.format(count)
  
def save_data(task, trial_records):
  if CONTEXT['store_data']:
    task_data = dataclasses.asdict(TaskData(trial_records, task.get_key_events()))
    if 'trajectories' in CONTEXT:
      task_data['trajectories'] = CONTEXT['trajectories']
    
    filename = '{}.json'.format(datetime.now().strftime('%m_%d_%Y_%H_%M_%S'))
    filep = os.path.join(os.getcwd(), 'data', filename)
    with open(filep, 'w') as f:
      f.write(json.dumps(task_data))

def get_identity_collider_bounds(collider):
  return collider

def get_balloon_collider_bounds(collider):
  h = collider[3] - collider[1]
  w = collider[2] - collider[0]
  ws = 0.25
  y1 = collider[1] + h
  y0 = y1 - h * 0.5
  x0 = collider[0] + w * 0.5 - w * ws
  x1 = collider[0] + w * 0.5 + w * ws  
  return [x0, y0, x1, y1]

def load_yoke_file(yf: str):
  if yf.endswith('.pickle'):
    with open(yf, 'rb') as f:
      return data.decode_pickled_yoke_file(f)
  else:
    with open(yf, 'rt') as f:
      return data.decode_json_yoke_file_source(f.read())

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--difficulty', choices=['easy', 'medium', 'hard', 'extra_hard', 'debug'])
  parser.add_argument('-t', '--task', choices=['egg', 'balloon', 'iceberg'], default='balloon')
  parser.add_argument('-ao', '--avoid_only', action='store_true', default=False)
  parser.add_argument('-nd', '--no_data', action='store_true', default=False)
  parser.add_argument('-dt', '--debug_target', action='store_true', default=False)
  parser.add_argument('-dk', '--debug_keys', action='store_true', default=False)
  parser.add_argument('-yf', '--yoke_file')
  return parser.parse_args()
  
def main():
  args = parse_args()  

  TASK_TYPE = args.task
  CONTEXT['difficulty'] = args.difficulty
  CONTEXT['avoid_only'] = args.avoid_only
  CONTEXT['store_data'] = not args.no_data

  if args.debug_keys:
    set_debug_keys()

  max_num_trials = int(1e6)
  num_trials = DEBUG_NUM_TRIALS
  trajectories = None

  # Optionally load a prior participant's results to yoke-to.
  yoke_to = None
  if args.yoke_file is not None:
    yoke_to = load_yoke_file(args.yoke_file)
    max_num_trials = len(yoke_to)

  # Load the predefined trajectories for this run corresponding to the specified difficulty.
  if not args.difficulty == 'debug':
    trajectories = data.load_trajectories(args.difficulty)
    num_trials = min(max_num_trials, len(trajectories['signs']))
    CONTEXT['trajectories'] = trajectories

  win = create_window()
  task = Task(win, lambda loop_res: KEY_MAP['stop'] in loop_res.keys)

  get_collider_bounds = get_identity_collider_bounds
  if TASK_TYPE == 'egg':
    task_stimuli = create_egg_stimuli(win)
    movement_info = make_egg_movement_info(task_stimuli)

  elif TASK_TYPE == 'balloon':
    task_stimuli = create_balloon_stimuli(win)
    movement_info = make_balloon_movement_info(task_stimuli, trajectories)
    get_collider_bounds = get_balloon_collider_bounds

  else:
    task_stimuli = create_iceberg_stimuli(win)
    movement_info = make_iceberg_movement_info(task_stimuli)

  wand = util.create_image_stim(win, res_path('images/magic_wand.png'))
  sparkle = util.create_image_stim(win, res_path('images/magic_effect.png'))
  iti_background = create_fullscreen_image_stim(win, res_path('images/iti_background.jpg'))
  debug_collider_bounds_stim = util.create_rect_stim(win) if args.debug_target else None

  counter_stim = util.create_text_stim(win, 'spells cast: 0', height=32.0)
  counter_stim.setPos([SCREEN_WIDTH * 0.5 - 150, SCREEN_HEIGHT * 0.5 - 75])
  counter_background = util.create_rect_stim(win, width=195., height=48.)
  counter_background.setColor((0, 0, 0), 'rgb255')
  counter_background.setPos(counter_stim.pos[:])

  aversive_sound = util.create_sound(res_path('sounds/balloon_pop.wav'))
  pleasant_sound = util.create_sound(res_path('sounds/magic_sound.wav'))

  spells_cast = 0
  trial_records: List[data.TrialRecord] = []

  for trial in range(num_trials):
    present_result = None
    if not CONTEXT['avoid_only']:
      present_result = states.static(task, [task_stimuli['background0']], t=1)

    collider_movement = movement_info['get_movement'](trial)
    yoke_trial = None if yoke_to is None else yoke_to[trial]

    interact_result = states.interactive_collider(
      task=task,
      key_map=KEY_MAP, 
      move_increment=MOVE_INCR_PX,
      always_draw_stimuli=[task_stimuli['background1'], wand, counter_background, counter_stim],
      aversive_sound=aversive_sound,
      pleasant_sound=pleasant_sound,
      play_aversive_sound='conditionally',
      counter_stim=counter_stim,
      get_counter_stim_text=get_counter_stim_text_fn(trial),
      counter_value=spells_cast,
      implement_stim=wand, implement_pos=[0, -SCREEN_HEIGHT * 0.5 + wand.height * 0.5 + BORDER_WIDTH],
      collider_stim=task_stimuli['collider_stim'],
      collided_stim=task_stimuli['collided_stim'],
      collider_pos=collider_movement.initial_position(),
      collider_movement=collider_movement, 
      collider_reached_target=movement_info['reached_target'],
      sparkle_stim=sparkle, 
      get_collider_bounds=get_collider_bounds, 
      debug_collider_bounds_stim=debug_collider_bounds_stim,
      yoke_to=yoke_trial,
      t=8)

    iti_result = None
    if not CONTEXT['avoid_only']:
      iti_result = states.static(task, [iti_background], t=10)

    trial_records.append(TrialRecord(present_result, interact_result, iti_result))

    if interact_result.implement_hit_collider:
      spells_cast += 1
    
    if task.pending_abort:
      print('Aborting trial sequence.')
      break

  save_data(task, trial_records)

  win.close()
  core.quit()

if __name__ == '__main__':
  main()