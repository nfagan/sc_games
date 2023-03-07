import util

class InteractStateResult(object):
  def __init__(self, implement_hit_collider):
    self.implement_hit_collider = implement_hit_collider

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
    _ = task.loop()

def interactive_collider(*,
  task, key_map, move_increment,
  always_draw_stimuli, 
  aversive_sound, pleasant_sound,
  play_aversive_sound,
  counter_stim, counter_value,
  implement_stim, implement_pos, 
  collider_stim, collided_stim, collider_pos, collider_movement, collider_reached_target, 
  sparkle_stim, t):
  #
  assert play_aversive_sound in ['always', 'never', 'conditionally']

  implement_hit_collider = False
  collider_did_reach_target = False

  implement_stim.setPos(implement_pos)
  collider_stim.setPos(collider_pos)

  task.enter_state()
  while task.state_time() < t:
    counter_stim.text = 'spells cast: {}'.format(counter_value)

    for stim in always_draw_stimuli:
      stim.draw()

    if implement_hit_collider:
      sparkle_stim.draw()

    if collider_did_reach_target and not implement_hit_collider:
      collided_stim.draw()
    else:
      collider_stim.draw()

    res = task.loop()
    move = parse_key_movement(key_map, res.keys)
    if move is not None:
      implement_pos = [x + y * float(move_increment) for x, y in zip(implement_pos, move)]
      implement_stim.setPos(implement_pos)

    ft = max(0., min(1., task.state_time() / t))
    collider_move = collider_movement.tick(res.dt, ft, collider_pos, collider_did_reach_target)
    collider_pos = [x + y for x, y in zip(collider_pos, collider_move)]

    if not collider_did_reach_target and collider_reached_target(collider_pos):
      collider_did_reach_target = True
      if play_aversive_sound == 'always' or \
        (play_aversive_sound == 'conditionally' and not implement_hit_collider):
        aversive_sound.play()

    collider_stim.setPos(collider_pos)
    sparkle_stim.setPos(collider_pos)
    collided_stim.setPos(collider_pos)

    collider_bounds = util.stimulus_bounding_box(collider_stim)
    implement_bounds = util.stimulus_bounding_box(implement_stim)

    if util.bounding_boxes_intersect(collider_bounds, implement_bounds):
      if not implement_hit_collider:
        counter_value += 1
        pleasant_sound.play()      
      implement_hit_collider = True

  return InteractStateResult(implement_hit_collider)