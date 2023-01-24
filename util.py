from psychopy import visual, sound

def stimulus_bounding_box(stim):
  pos = stim.pos
  x0 = pos[0] - stim.width * 0.5
  x1 = x0 + stim.width
  y0 = pos[1] - stim.height * 0.5
  y1 = y0 + stim.height
  return [x0, y0, x1, y1]

def bounding_box_center(rect):
  w = rect[2] - rect[0]
  h = rect[3] - rect[1]
  return [rect[0] + w * 0.5, rect[1] + h * 0.5]

def bounding_boxes_intersect(r0, r1):
  x0 = max(r0[0], r1[0])
  y0 = max(r0[1], r1[1])
  x1 = min(r0[2], r1[2])
  y1 = min(r0[3], r1[3])
  lx = x1 - x0
  if lx <= 0:
    return False
  ly = y1 - y0
  if ly <= 0:
    return False
  return True

def create_text_stim(win, text):
  return visual.TextStim(win, text)

def create_image_stim(win, file_path, width=None, height=None):
  stim = visual.ImageStim(
    win, units='pix', image=file_path, pos=[0, 0], interpolate=True, depth=-4.0)
  if width is not None:
    stim.width = width
  if height is not None:
    stim.height = height
  return stim

def create_rect_stim(win):
  return visual.Rect(win, pos=[0, 0], width=64, height=64, units='pix', fillColor=[255, 0, 0])

def create_sound(file_path):
  return sound.Sound(file_path, secs=-1, volume=1.0)