from task import Task
import states
import util
from psychopy import visual, core
import os
from os import path

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FULL_SCREEN = False
RES_ROOT = path.join(os.getcwd(), 'res')
KEY_MAP = {
  'move_left': 'a',
  'move_right': 'd',
  'move_down': 's',
  'move_up': 'w'
}
MOVE_INCR_PX = 20
ICEBERG_VEL_PX = 120

def res_path(p):
  return path.join(RES_ROOT, p)

def create_window():
  return visual.Window(
    size=(SCREEN_WIDTH, SCREEN_HEIGHT), monitor = 'testMonitor', allowGUI=False, 
    fullscr=FULL_SCREEN, useFBO=False, units='pix')

def create_fullscreen_image_stim(win, p):
  return util.create_image_stim(win, p, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
  
def main():
  win = create_window()
  task = Task(win)

  wand = util.create_image_stim(win, res_path('images/magic_wand.png'))
  iceberg = util.create_image_stim(win, res_path('images/orange_hand.png'))
  ship = util.create_image_stim(win, res_path('images/cracking_egg_1.png'))
  sparkle = util.create_image_stim(win, res_path('images/magic_effect.png'))
  background0 = create_fullscreen_image_stim(win, res_path('images/Balloon_anticipatory_background.jpg'))
  background1 = create_fullscreen_image_stim(win, res_path('images/Balloon_avoidance_background.jpg'))
  fix_background = create_fullscreen_image_stim(win, res_path('images/iti_background.png'))

  counter_stim = util.create_text_stim(win, 'spells cast: 0')
  counter_stim.setPos([-SCREEN_WIDTH * 0.5 + 100, SCREEN_HEIGHT * 0.5 - 100])

  aversive_sound = util.create_sound(res_path('sounds/balloon_pop.wav'))
  pleasant_sound = util.create_sound(res_path('sounds/magic_sound.wav'))

  spells_cast = 0
  for _ in range(2):
    states.static(task, [background0], t=1)

    interact_result = states.iceberg_interact(
      task=task,
      key_map=KEY_MAP, 
      move_increment=MOVE_INCR_PX,
      drawables=[background1, wand, iceberg, ship, counter_stim],
      aversive_sound=aversive_sound, 
      pleasant_sound=pleasant_sound,
      counter_stim=counter_stim,
      counter_value=spells_cast,
      wand_stim=wand, wand_pos=[0, 0], 
      collider_stim=iceberg, collider_pos=[0, 200],
      collider_vel=ICEBERG_VEL_PX, collider_edge=-SCREEN_HEIGHT * 0.5,
      sparkle_stim=sparkle, 
      t=8)

    states.static(task, [fix_background], t=10)

    if interact_result.wand_hit_collider:
      spells_cast += 1

  win.close()
  core.quit()

if __name__ == '__main__':
  main()