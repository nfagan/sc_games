from task import Task
import states
import util
import data
import trajectory
from movement import ZigMovement, KeypointMovement
from psychopy import visual, core
import argparse
import os
from os import path

DEBUG_NUM_TRIALS = 8
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
BORDER_WIDTH = 30 # pixels, width of yellow/purple border; approximate.
FULL_SCREEN = False
RES_ROOT = path.join(os.getcwd(), 'res')
KEY_MAP = {
  'move_left': 'a',
  'move_right': 'd',
  'move_down': 's',
  'move_up': 'w',
  'stop': 'escape'
}
MOVE_INCR_PX = 80
TASK_TYPE = 'balloon'
CONTEXT = {'difficulty': '', 'trajectories': None}

def res_path(p):
  return path.join(RES_ROOT, p)

def create_window():
  return visual.Window(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT), monitor = 'testMonitor', allowGUI=False, 
    fullscr=FULL_SCREEN, useFBO=False, units='pix')

def create_fullscreen_image_stim(win, p):
  return util.create_image_stim(win, p, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)

def create_balloon_stimuli(win):
  return {
    'background0': create_fullscreen_image_stim(win, res_path('images/Balloon_anticipatory_background.jpg')),
    'background1': create_fullscreen_image_stim(win, res_path('images/Balloon_avoidance_background.jpg')),
    'collider_stim': util.create_image_stim(win, res_path('images/pink_balloon.png')),
    'collided_stim': util.create_image_stim(win, res_path('images/pop_1.png'))
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

def gen_keypoints(trial):
  if CONTEXT['trajectories'] is not None:
    kps = CONTEXT['trajectories']['points'][trial][:]
  else:
    kp_fns = [trajectory.easy, trajectory.med, trajectory.hard, trajectory.extra_hard]
    kp_fn = kp_fns[trial % len(kp_fns)]
    kps = kp_fn()
  kps = [[x[0] * SCREEN_WIDTH * 0.5, x[1] * SCREEN_HEIGHT * 0.5] for x in kps]
  return kps

def make_balloon_movement_info(stimuli):
  if True:
    get_movement = lambda tn: KeypointMovement(gen_keypoints(tn))
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
  
def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--difficulty', choices=['easy', 'medium', 'hard', 'extra_hard', 'debug'])
  parser.add_argument('-t', '--task', choices=['egg', 'balloon', 'iceberg'], default='balloon')
  parser.add_argument('-ao', '--avoid_only', action='store_true', default=False)
  args = parser.parse_args()

  TASK_TYPE = args.task
  CONTEXT['difficulty'] = args.difficulty
  CONTEXT['avoid_only'] = args.avoid_only

  num_trials = DEBUG_NUM_TRIALS
  if not args.difficulty == 'debug':
    CONTEXT['trajectories'] = data.load_trajectories(args.difficulty)
    num_trials = len(CONTEXT['trajectories']['signs'])

  win = create_window()
  task = Task(win, lambda loop_res: KEY_MAP['stop'] in loop_res.keys)

  if TASK_TYPE == 'egg':
    task_stimuli = create_egg_stimuli(win)
    movement_info = make_egg_movement_info(task_stimuli)

  elif TASK_TYPE == 'balloon':
    task_stimuli = create_balloon_stimuli(win)
    movement_info = make_balloon_movement_info(task_stimuli)

  else:
    task_stimuli = create_iceberg_stimuli(win)
    movement_info = make_iceberg_movement_info(task_stimuli)

  wand = util.create_image_stim(win, res_path('images/magic_wand.png'))
  sparkle = util.create_image_stim(win, res_path('images/magic_effect.png'))
  iti_background = create_fullscreen_image_stim(win, res_path('images/iti_background.jpg'))

  counter_stim = util.create_text_stim(win, 'spells cast: 0')
  counter_stim.setPos([-SCREEN_WIDTH * 0.5 + 100, SCREEN_HEIGHT * 0.5 - 100])

  aversive_sound = util.create_sound(res_path('sounds/balloon_pop.wav'))
  pleasant_sound = util.create_sound(res_path('sounds/magic_sound.wav'))

  spells_cast = 0
  for trial in range(num_trials):
    if not CONTEXT['avoid_only']:
      states.static(task, [task_stimuli['background0']], t=1)

    collider_movement = movement_info['get_movement'](trial)
    
    interact_result = states.interactive_collider(
      task=task,
      key_map=KEY_MAP, 
      move_increment=MOVE_INCR_PX,
      always_draw_stimuli=[task_stimuli['background1'], wand, counter_stim],
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
      t=8)

    if not CONTEXT['avoid_only']:
      states.static(task, [iti_background], t=10)

    if interact_result.implement_hit_collider:
      spells_cast += 1
    
    if task.pending_abort:
      print('Aborting trial sequence.')
      break

  win.close()
  core.quit()

if __name__ == '__main__':
  main()