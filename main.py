from task import Task
import states
import util
import data
import trajectory
from movement import ZigMovement, KeypointMovement
from psychopy import visual, core
import os
from os import path

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900
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

def gen_trajectory(gen_traj):
  while True:
    kps = gen_traj()
    accept = all(map(lambda kp: kp[0] >= -1. and kp[0] <= 1. and kp[1] >= -1. and kp[1] <= 1., kps))
    if accept:
      return kps

def hard_trajectory():
  return gen_trajectory(
    lambda: trajectory.gen_trajectory(nsteps=6, x_step_min=0.3, x_step_max=1., y_sigma=0.05))

def med_trajectory():
  return gen_trajectory(
    lambda: trajectory.gen_trajectory(nsteps=3, x_step_min=0.4, x_step_max=0.8, y_sigma=0.025))

def easy_trajectory():
  return gen_trajectory(
    lambda: trajectory.gen_trajectory(nsteps=2, x_step_min=0.2, x_step_max=0.4, y_sigma=0.025))

def make_balloon_movement_info(stimuli):
  if True:
    # kps = easy_trajectory()
    kps = med_trajectory()
    # kps = hard_trajectory()

    kps = [[x[0] * SCREEN_WIDTH * 0.5, x[1] * SCREEN_HEIGHT * 0.5] for x in kps]
    get_movement = lambda tn: KeypointMovement(kps[:])
    get_position = lambda tn: kps[0]    

  else:
    get_movement = lambda tn: ZigMovement(data.balloon_velocity(tn), data.balloon_zigs(tn))
    get_position = lambda tn: data.balloon_position(tn, SCREEN_HEIGHT)

  return {
    'get_movement': get_movement,
    'get_position': get_position,
    'reached_target': lambda pos: pos[1] > SCREEN_HEIGHT * 0.5 - stimuli['collider_stim'].height * 0.5
  }

def make_egg_movement_info(stimuli):
  return {
    'get_movement': lambda tn: ZigMovement(data.egg_velocity(tn), data.egg_zigs(tn)),
    'get_position': lambda tn: [0, SCREEN_HEIGHT * 0.5],
    'reached_target': lambda pos: pos[1] < -SCREEN_HEIGHT * 0.5 + stimuli['collider_stim'].height * 0.5
  }

def make_iceberg_movement_info(stimuli):
  return make_egg_movement_info(stimuli)
  
def main():
  assert TASK_TYPE in ['egg', 'balloon', 'iceberg']

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
  for trial in range(4):
    states.static(task, [task_stimuli['background0']], t=1)

    interact_result = states.interactive_collider(
      task=task,
      key_map=KEY_MAP, 
      move_increment=MOVE_INCR_PX,
      always_draw_stimuli=[task_stimuli['background1'], wand, counter_stim],
      aversive_sound=aversive_sound,
      pleasant_sound=pleasant_sound,
      play_aversive_sound='conditionally',
      counter_stim=counter_stim,
      counter_value=spells_cast,
      implement_stim=wand, implement_pos=[0, -SCREEN_HEIGHT * 0.5 + 40.],
      collider_stim=task_stimuli['collider_stim'],
      collided_stim=task_stimuli['collided_stim'],
      collider_pos=movement_info['get_position'](trial),
      collider_movement=movement_info['get_movement'](trial), 
      collider_reached_target=movement_info['reached_target'],
      sparkle_stim=sparkle, 
      t=8)

    states.static(task, [iti_background], t=2)

    if interact_result.implement_hit_collider:
      spells_cast += 1
    
    if task.pending_abort:
      print('Aborting trial sequence.')
      break

  win.close()
  core.quit()

if __name__ == '__main__':
  main()