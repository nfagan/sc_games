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
    return balloon_trajectory_info[tn][4]
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