import util

class InteractStateResult(object):
  def __init__(self, wand_hit_collider):
    self.wand_hit_collider = wand_hit_collider

def parse_key_movement(key_map, keys):
  if key_map['move_left'] in keys:
    return [-1, 0]
  elif key_map['move_right'] in keys:
    return [1, 0]
  elif key_map['move_down'] in keys:
    return [0, -1]
  elif key_map['move_up'] in keys:
    return [0, 1]
  else:
    return None

def static(task, drawables, t):
  task.enter_state()
  while task.state_time() < t:
    for stim in drawables:
      stim.draw()
    res = task.loop()

def iceberg_interact(
  task, key_map, move_increment, drawables, aversive_sound, pleasant_sound, counter_stim, counter_value,
  wand_stim, wand_pos, collider_stim, collider_pos, collider_vel, collider_edge, sparkle_stim, t):
  #
  wand_hit_collider = False

  task.enter_state()
  while task.state_time() < t:
    counter_stim.text = 'spells cast: {}'.format(counter_value)

    for stim in drawables:
      stim.draw()

    if wand_hit_collider:
      sparkle_stim.draw()

    res = task.loop()
    move = parse_key_movement(key_map, res.keys)
    if move is not None:
      wand_pos = [x + y * float(move_increment) for x, y in zip(wand_pos, move)]
      wand_stim.setPos(wand_pos)

    collider_pos[1] -= res.dt * collider_vel
    if collider_pos[1] < collider_edge:
      aversive_sound.play()
      break

    collider_stim.setPos(collider_pos)
    sparkle_stim.setPos(collider_pos)

    collider_bounds = util.stimulus_bounding_box(collider_stim)
    wand_bounds = util.stimulus_bounding_box(wand_stim)

    if util.bounding_boxes_intersect(collider_bounds, wand_bounds):
      if not wand_hit_collider:
        counter_value += 1
        pleasant_sound.play()      
      wand_hit_collider = True

  return InteractStateResult(wand_hit_collider)