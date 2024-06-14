from task import Task
from common_types import TaskData, TrialRecord
import states
import util
import data
import trajectory
from labjack import LabJack
from mri import MRIInterface
from movement import ZigMovement, KeypointMovement
from psychopy import visual, core
import argparse
import os
from os import path
import sys
from typing import List, Tuple
import dataclasses
from datetime import datetime
import json

SCREEN_INFO = {
  'width': 1440,
  'height': 900,
  'fullscreen': False
}
DEBUG_NUM_TRIALS = 8
BORDER_WIDTH = 30 # pixels, width of yellow/purple border; approximate.
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

# height of icebergs at bottom of screen
ICEBERG_OFFSET_PX = 120

def screen_width() -> int:
  return SCREEN_INFO['width']

def screen_height() -> int:
  return SCREEN_INFO['height']

def is_full_screen() -> bool:
  return SCREEN_INFO['fullscreen']

def set_debug_keys():
  KEY_MAP['move_left'] = 'a'
  KEY_MAP['move_right'] = 'd'
  KEY_MAP['move_up'] = 'w'
  KEY_MAP['move_down'] = 's'

def res_path(p):
  return path.join(RES_ROOT, p)

def create_window():
  return visual.Window(
    size=(screen_width(), screen_height()), monitor = 'testMonitor', allowGUI=False, 
    fullscr=is_full_screen(), useFBO=False, units='pix')

def create_fullscreen_image_stim(win, p):
  return util.create_image_stim(win, p, width=screen_width(), height=screen_height())

def create_balloon_stimuli(win):
  string_suffix = '_no_string'
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Balloon_anticipatory_background.jpg')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Balloon_avoidance_background.jpg')),
    'collider_stim': util.create_image_stim(win, res_path('images/pink_balloon{}.png'.format(string_suffix))),
    'collided_stim': util.create_image_stim(win, res_path('images/pop_1{}.png'.format(string_suffix))),
    'aversive_sound': util.create_sound(res_path('sounds/balloon_pop.wav')),
    'pleasant_sound': util.create_sound(res_path('sounds/magic_sound.wav'))
  }

def create_egg_stimuli(win):
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Egg_anticipatory_background.jpg')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Egg_avoidance_background.jpg')),
    'collider_stim': util.create_image_stim(win, res_path('images/egg.png')),
    'collided_stim': util.create_image_stim(win, res_path('images/cracking_egg_1.png')),
    'aversive_sound': util.create_sound(res_path('sounds/egg_crack.wav')),
    'pleasant_sound': util.create_sound(res_path('sounds/magic_sound.wav'))
  }

def create_iceberg_stimuli(win):
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/iceberg_background_Anticipatory.png')),
    'background1': create_fullscreen_image_stim(win, res_path('images/iceberg_background_Avoidance.png')),
    'collider_stim': util.create_image_stim(win, res_path('images/boat_stim_120_150.png')),
    'collided_stim': util.create_image_stim(win, res_path('images/boat_stim_broken_120_150.png')),
    'aversive_sound': util.create_sound(res_path('sounds/boat_smash.wav')),
    'pleasant_sound': util.create_sound(res_path('sounds/magic_sound.wav'))
  }

def gen_keypoints(trial, trajectories):
  if trajectories is not None:
    kps = trajectories['points'][trial][:]
  else:
    kp_fns = [trajectory.easy, trajectory.med, trajectory.hard, trajectory.extra_hard]
    kp_fn = kp_fns[trial % len(kp_fns)]
    kps = kp_fn()
  kps = [[x[0] * screen_width() * 0.5, x[1] * screen_height() * 0.5] for x in kps]
  return kps

def make_balloon_movement_info(stimuli, trajectories):
  if True:
    get_movement = lambda tn: KeypointMovement(gen_keypoints(tn, trajectories))
  else:
    get_movement = lambda tn: ZigMovement(
      data.balloon_position(tn, screen_height()), data.balloon_velocity(tn), data.balloon_zigs(tn))
  return {
    'get_movement': get_movement,
    'reached_target': lambda pos: pos[1] > screen_height() * 0.5 - stimuli['collider_stim'].height * 0.5
  }

def make_egg_movement_info(stimuli):
  p0 = [0, screen_height() * 0.5]
  return {
    'get_movement': lambda tn: ZigMovement(p0, data.egg_velocity(tn), data.egg_zigs(tn)),
    'reached_target': lambda pos: pos[1] < -screen_height() * 0.5 + stimuli['collider_stim'].height * 0.5
  }

def make_iceberg_movement_info(stimuli, trajectories):
  # height of icebergs at bottom of screen
  iceberg_offset = ICEBERG_OFFSET_PX
  # factor by which movement should be slowed to account for the boat hitting the iceberg sooner,
  # compared to the balloon game, because of the above offset.
  speed_scale = (screen_height() - iceberg_offset) / screen_height()
  get_movement = lambda tn: KeypointMovement(gen_keypoints(tn, trajectories), speed_scale=speed_scale)
  return {
    'get_movement': get_movement,
    'reached_target': lambda pos: pos[1] < -screen_height() * 0.5 + stimuli['collider_stim'].height * 0.5 + iceberg_offset
  }

def get_counter_stim_text_fn(trial):
  if CONTEXT['difficulty'] == 'debug':
    trial_difficulty = ['easy', 'medium', 'hard', 'extra-hard'][trial % 4]
    return lambda count: '({}) spells cast: {}'.format(trial_difficulty, count)
  else:
    return lambda count: 'spells cast: {}'.format(count)
  
def str_timestamp():
  return datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
  
def save_data(task: Task, trial_records, command_line: str):
  if not CONTEXT['store_data']:
    return
  
  part_id = '' if 'participant_id' not in CONTEXT else CONTEXT['participant_id']
  
  task_data = dataclasses.asdict(TaskData(trial_records, task.get_key_events()))
  opt_args = ['trajectories', 'participant_id', 'yoke_file']
  for arg in opt_args:
    task_data[arg] = CONTEXT[arg] if arg in CONTEXT else None

  task_data['mri_trs'] = task.get_mri_trs()
  task_data['command_line'] = command_line
  
  filename = 'participant_id_{}-{}.json'.format(part_id, str_timestamp())
  filep = os.path.join(os.getcwd(), 'data', filename)
  with open(filep, 'w') as f:
    f.write(json.dumps(task_data))

  orig_data = data.convert_json_trial_data_to_original_data_structure(task_data, True)
  orig_filep = os.path.join(os.getcwd(), 'data', 'original_format', filename.replace('.json', '.txt'))
  with open(orig_filep, 'w') as f:
    f.write(orig_data)

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

def flip_trajectory_y_axis(ps: List[List[Tuple[int, int]]]):
  for i in range(len(ps)):
    for j in range(len(ps[i])):
      ps[i][j][1] *= -1

def load_yoke_file(yf: str):
  if yf.endswith('.pickle'):
    with open(yf, 'rb') as f:
      return data.decode_pickled_yoke_file(f)
  else:
    with open(yf, 'rt') as f:
      return data.decode_json_yoke_file_source(f.read())
    
def create_labjack(enable: bool) -> LabJack:
  log_file_p = os.path.join(os.getcwd(), 'data/log/log-{}.txt'.format(str_timestamp()))
  labjack_events = {"avoidance_onset": 4, "first_contact": 5, "aversive_sound": 6, "no_aversive_sound": 7, "target_frozen": 7}
  labjack_impl = LabJack(enable=enable, events=labjack_events, log_file_path=log_file_p)
  return labjack_impl

def create_mri_interface(enable: bool) -> MRIInterface:
  return MRIInterface(enable)

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--difficulty', choices=['easy', 'medium', 'hard', 'extra_hard', 'debug'])
  parser.add_argument('-t', '--task_type', choices=['egg', 'balloon', 'iceberg'], default='balloon')
  parser.add_argument('-ao', '--avoid_only', action='store_true', default=False)
  parser.add_argument('-nd', '--no_data', action='store_true', default=False)
  parser.add_argument('-dt', '--debug_target', action='store_true', default=False)
  parser.add_argument('-dk', '--debug_keys', action='store_true', default=False)
  parser.add_argument('-yf', '--yoke_file')
  parser.add_argument('-pid', '--participant_id')
  parser.add_argument('-nlj', '--no_labjack', action='store_true', default=False)
  parser.add_argument('-mri', '--mri', action='store_true', default=False)
  parser.add_argument('-sw', '--screen_width')
  parser.add_argument('-sh', '--screen_height')
  parser.add_argument('-fs', '--full_screen', action='store_true', default=False)
  return parser.parse_args()

def set_screen_info(args):
  if args.full_screen:
    SCREEN_INFO['fullscreen'] = True
  if args.screen_width is not None:
    SCREEN_INFO['width'] = int(args.screen_width)
  if args.screen_height is not None:
    SCREEN_INFO['height'] = int(args.screen_height)

def create_instruction_slides(win, task_type: str, is_mirrored: bool):
  if is_mirrored or task_type != 'balloon':
    instr_folder = f'mirrored_instructions/{task_type}'
    instr_prefix = 'Slide'
    instr_slide_info = [
      {'p': 'images/{}/{}1.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}2.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}3.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}4.png'.format(instr_folder, instr_prefix), 'key': KEY_MAP['move_left']},
      {'p': 'images/{}/{}5.png'.format(instr_folder, instr_prefix), 'key': KEY_MAP['move_up']},
      {'p': 'images/{}/{}6.png'.format(instr_folder, instr_prefix), 'key': KEY_MAP['move_right']},
      {'p': 'images/{}/{}7.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}8.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}9.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}10.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}11.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}11.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}12.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}13.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}14.png'.format(instr_folder, instr_prefix), 'key': 'space'},
      {'p': 'images/{}/{}15.png'.format(instr_folder, instr_prefix), 'key': 'space'},
    ]

  else:
    instr_folder = f'instructions/{task_type}'
    instr_prefix = 'instruction' if task_type == 'balloon' else 'Slide'
    num_slides = 11 if task_type == 'balloon' else 15  
    instr_slide_info = [
      {'p': 'images/{}/{}{}.png'.format(instr_folder, instr_prefix, x), 'key': 'space'} for x in range(1, num_slides)
    ]

  for slide in instr_slide_info:
    slide['stim'] = create_fullscreen_image_stim(win, res_path(slide['p']))

  return instr_slide_info
  
def main():
  command_line = ' '.join(sys.argv)

  args = parse_args()
  set_screen_info(args)

  TASK_TYPE = args.task_type
  CONTEXT['difficulty'] = args.difficulty
  CONTEXT['avoid_only'] = args.avoid_only
  CONTEXT['store_data'] = not args.no_data
  CONTEXT['participant_id'] = args.participant_id
  CONTEXT['yoke_file'] = args.yoke_file

  if args.debug_keys:
    set_debug_keys()

  labjack = create_labjack(not args.no_labjack)
  labjack_event_handler = lambda identifier, time: labjack.send_event(identifier, time)

  mri_interface = create_mri_interface(args.mri)

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
  task = Task(
    window=win, 
    abort_crit=lambda loop_res: KEY_MAP['stop'] in loop_res.keys,
    mri_interface=mri_interface)

  get_collider_bounds = get_identity_collider_bounds
  is_controllable = False
  if TASK_TYPE == 'egg':
    task_stimuli = create_egg_stimuli(win)
    movement_info = make_egg_movement_info(task_stimuli)

  elif TASK_TYPE == 'balloon':
    task_stimuli = create_balloon_stimuli(win)
    movement_info = make_balloon_movement_info(task_stimuli, trajectories)
    get_collider_bounds = get_balloon_collider_bounds
    is_controllable = True

  else:
    assert TASK_TYPE == 'iceberg'
    flip_trajectory_y_axis(trajectories['points'])
    task_stimuli = create_iceberg_stimuli(win)
    movement_info = make_iceberg_movement_info(task_stimuli, trajectories)

  wand = util.create_image_stim(win, res_path('images/magic_wand.png'))
  sparkle = util.create_image_stim(win, res_path('images/magic_effect.png'))
  iti_background = create_fullscreen_image_stim(win, res_path('images/iti_background.jpg'))
  debug_collider_bounds_stim = util.create_rect_stim(win) if args.debug_target else None

  counter_stim = util.create_text_stim(win, 'spells cast: 0', height=32.0)
  counter_stim.setPos([screen_width() * 0.5 - 150, screen_height() * 0.5 - 75])
  counter_background = util.create_rect_stim(win, width=195., height=48.)
  counter_background.setColor((0, 0, 0), 'rgb255')
  counter_background.setPos(counter_stim.pos[:])

  spells_cast = 0
  trial_records: List[data.TrialRecord] = []

  # instructions
  instr_slides = create_instruction_slides(win, TASK_TYPE, is_mirrored=args.mri)
  for slide in instr_slides:
    states.key_press(task, slide['key'], [slide['stim']])

  # main task
  for trial in range(num_trials):
    task.wait_for_mri_tr(task.task_time())  # wait for next TR

    present_result = None
    if not CONTEXT['avoid_only']:
      present_result = states.static(task, [task_stimuli['background0']], t=1)

    collider_movement = movement_info['get_movement'](trial)
    collider_movement.reset()

    yoke_trial = None if yoke_to is None else yoke_to[trial]

    interact_result = states.interactive_collider(
      task=task,
      is_controllable=is_controllable,
      key_map=KEY_MAP, 
      move_increment=MOVE_INCR_PX,
      always_draw_stimuli=[task_stimuli['background1'], wand, counter_background, counter_stim],
      aversive_sound=task_stimuli['aversive_sound'],
      pleasant_sound=task_stimuli['pleasant_sound'],
      play_aversive_sound='conditionally',
      counter_stim=counter_stim,
      get_counter_stim_text=get_counter_stim_text_fn(trial),
      counter_value=spells_cast,
      implement_stim=wand, implement_pos=[0, -screen_height() * 0.5 + wand.height * 0.5 + BORDER_WIDTH],
      collider_stim=task_stimuli['collider_stim'],
      collided_stim=task_stimuli['collided_stim'],
      collider_pos=collider_movement.initial_position(),
      collider_movement=collider_movement, 
      collider_reached_target=movement_info['reached_target'],
      sparkle_stim=sparkle, 
      get_collider_bounds=get_collider_bounds, 
      debug_collider_bounds_stim=debug_collider_bounds_stim,
      yoke_to=yoke_trial,
      event_handler=labjack_event_handler,
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

  labjack.shutdown()
  save_data(task, trial_records, command_line)

  win.close()
  core.quit()

if __name__ == '__main__':
  main()