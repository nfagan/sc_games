import util
from task import Task
from common_types import YokeRecord, MovementHistoryRecord, InteractStateResult, StaticStateResult
from typing import Optional, List, Callable

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

def static(task: Task, drawables, t):
  entry_t = task.task_time()
  task.enter_state()
  while task.state_time() < t:
    for stim in drawables:
      stim.draw()
    _ = task.loop()
  exit_t = task.task_time()
  return StaticStateResult(entry_t, exit_t)

def _draw_debug_collider_bounds_stim(stim, bounds):
  stim.width = bounds[2] - bounds[0]
  stim.height = bounds[3] - bounds[1]
  x = bounds[0] + stim.width * 0.5
  y = bounds[1] + stim.height * 0.5
  stim.setPos([x, y])
  stim.draw()

def interactive_collider(*,
  task: Task, key_map, move_increment,
  always_draw_stimuli, 
  aversive_sound, pleasant_sound,
  play_aversive_sound,
  counter_stim, get_counter_stim_text, counter_value,
  implement_stim, implement_pos, 
  collider_stim, collided_stim, collider_pos, collider_movement, collider_reached_target, 
  get_collider_bounds, debug_collider_bounds_stim,
  event_handler: Callable[[str, float], None],
  sparkle_stim, t, yoke_to: Optional[YokeRecord]):
  #
  assert play_aversive_sound in ['always', 'never', 'conditionally']

  is_yoked = yoke_to is not None
  is_yoked_implement_hit_collider = is_yoked and yoke_to.implement_hit

  implement_move_history = [MovementHistoryRecord(task.task_time(), implement_pos[:], [0, 0])]
  implement_hit_collider = False
  implement_hit_timestamp = None

  collider_did_reach_target = False
  collider_hit_timestamp = None

  implement_stim.setPos(implement_pos)
  collider_stim.setPos(collider_pos)

  entry_time = task.task_time()
  collider_bounds = None

  task.enter_state()
  while task.state_time() < t:
    counter_stim.text = get_counter_stim_text(counter_value)

    for stim in always_draw_stimuli:
      stim.draw()

    if implement_hit_collider:
      sparkle_stim.draw()

    if collider_did_reach_target and not implement_hit_collider:
      collided_stim.draw()
    else:
      collider_stim.draw()

    if debug_collider_bounds_stim is not None and collider_bounds is not None:
      _draw_debug_collider_bounds_stim(debug_collider_bounds_stim, collider_bounds)

    res = task.loop()
    move = parse_key_movement(key_map, res.keys)

    if move is not None:
      implement_pos = [x + y * float(move_increment) for x, y in zip(implement_pos, move)]
      implement_stim.setPos(implement_pos)
      implement_move_history.append(
        MovementHistoryRecord(task.task_time(), implement_pos[:], move[:]))

    if not collider_did_reach_target:
      ft = max(0., min(1., task.state_time() / t))
      collider_move = collider_movement.tick(res.dt, ft, collider_pos, collider_did_reach_target)
      collider_pos = [x + y for x, y in zip(collider_pos, collider_move)]

    # Check for collision between collider and its target (e.g., top of screen in balloon task).
    evaluate_collider_hit = False
    if not collider_did_reach_target and collider_reached_target(collider_pos):
      if not is_yoked or (is_yoked and not is_yoked_implement_hit_collider):
        evaluate_collider_hit = True

    # Just hit the target, determine whether to play the aversive sound.
    if evaluate_collider_hit:
      collider_did_reach_target = True
      collider_hit_timestamp = task.task_time()

      if play_aversive_sound == 'always' or \
        (play_aversive_sound == 'conditionally' and not implement_hit_collider):
        aversive_sound.play()
        event_handler('aversive_sound', collider_hit_timestamp)
      else:
        event_handler('no_aversive_sound', collider_hit_timestamp)

    collider_stim.setPos(collider_pos)
    sparkle_stim.setPos(collider_pos)
    collided_stim.setPos(collider_pos)

    collider_bounds = get_collider_bounds(util.stimulus_bounding_box(collider_stim))
    implement_bounds = util.stimulus_bounding_box(implement_stim)

    # Check whether the implement has struck its target (e.g., check whether the wand has struck 
    # the balloon in the balloon task)
    evaluate_implement_hit = False
    if (not collider_did_reach_target) and (not implement_hit_collider):
      if is_yoked:
        if is_yoked_implement_hit_collider and task.state_time() >= yoke_to.timestamp:
          evaluate_implement_hit = True
      elif util.bounding_boxes_intersect(collider_bounds, implement_bounds):
        evaluate_implement_hit = True
    
    if evaluate_implement_hit:
      implement_hit_timestamp = task.task_time()
      event_handler('first_contact', implement_hit_timestamp)
      counter_value += 1
      pleasant_sound.play()
      implement_hit_collider = True

  exit_time = task.task_time()
  return InteractStateResult(
    entry_time, exit_time, 
    implement_move_history, implement_hit_collider, implement_hit_timestamp,
    collider_did_reach_target, collider_hit_timestamp)