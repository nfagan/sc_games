#!/usr/bin/env python2

from __future__ import absolute_import, division
import os, sys, re, pickle
from optparse import OptionParser

# screen size
screen_width = 1440
screen_height = 900

# image steps
image_1_step_size = 20
image_2_step_size = 1

parser = OptionParser() 
parser.add_option("-a", "--image-1", metavar="IMAGE", dest="image_1", help="one image")
parser.add_option("-b", "--image-2", metavar="IMAGE", dest="image_2", help="the other image")
parser.add_option("-o", "--output", metavar="FILE.pickle", dest="output_file", help="where to save the collision map pickle")
parser.add_option("-m", "--map", metavar="MAPFILE", dest="existing_map_file", help="supply an existing collision map file to pre-load (optional)")
(options, args) = parser.parse_args()

image_1_file = options.image_1
image_2_file = options.image_2
output_file = options.output_file
existing_map_file = options.existing_map_file

if not image_1_file or not image_2_file or not output_file:
    parser.print_help()
    sys.exit()

for file in (image_1_file, image_2_file):
    if not os.path.isfile(file):
        print "Error: Object file %s can't be found." % file
        sys.exit()

if not re.search("\.pickle$", output_file):
    print "Error: You must give your output file an extension of .pickle."
    sys.exit()

if os.path.dirname(output_file) == '':
    output_file = os.getcwd() + '/' + output_file
if not os.path.isdir(os.path.dirname(output_file)):
    print "Error: Your output file path isn't valid."
    sys.exit()
if os.path.isfile(output_file):
    print "Error: Your chosen output file already exists."
    sys.exit()

if existing_map_file:
    if not re.search("\.pickle$", existing_map_file):
        print "Error: The pre-existing collision map file doesn't seem to be a pickle (it should end in .pickle)."
        sys.exit()
    m = open(existing_map_file, 'r')
    starting_collision_space_by_y = pickle.load(m)
    starting_set = set()
    for y_coord in starting_collision_space_by_y.keys():
        for x_coord in range(starting_collision_space_by_y[y_coord][0], starting_collision_space_by_y[y_coord][1] + 1):
            starting_set.add((x_coord, y_coord))

from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

# Set up the window
win = visual.Window(size=(screen_width, screen_height), fullscr=True, monitor='testMonitor', blendMode='avg', useFBO=True)


args_1 = {"pos":(0,0)}
image_1 = visual.ImageStim(win=win, name='image_1', units='pix', image=image_1_file, pos=[0,0], interpolate=False, depth=-3.0)
image_1.autoDraw = True
image_2 = visual.ImageStim(win=win, name='image_2',units='pix', image=image_2_file, pos=[0,0], interpolate=False, depth=-2.0)
image_2.autoDraw = True
label = visual.TextStim(win=win, name='label', text=None, font='Arial', units='pix', pos=(550, -432), height=24, wrapWidth=None, ori=0, color='#053270', depth=-6.0)
label.autoDraw = True
border = visual.Rect(win, size=(screen_width*2, screen_height*2), units='pix', lineWidth = 30, lineColor = "red", opacity = 0)
border.autoDraw = True

collision_space = set() if not existing_map_file else starting_set
defining_collision = False

while True:
    # get current time
    xDist = image_1.pos[0] - image_2.pos[0]
    yDist = image_1.pos[1] - image_2.pos[1]
    label.setText("%d, %d" % (int(xDist), int(yDist)))
    
    if defining_collision:
        if (xDist, yDist) not in collision_space:
            collision_space.add((xDist, yDist))
        border.opacity = .75
    else:
        if (xDist, yDist) in collision_space:
            border.opacity = .75
        else:
            border.opacity = 0
    if event.getKeys(['right']):
        if image_1.pos[0] + image_1.size[0]/2 + image_1_step_size < screen_width/2:
            image_1.pos = (image_1.pos[0] + image_1_step_size, image_1.pos[1])
    elif event.getKeys(['left']):
        if image_1.pos[0] - image_1.size[0]/2 - image_1_step_size > -screen_width/2: 
            image_1.pos = (image_1.pos[0] - image_1_step_size, image_1.pos[1])
    elif event.getKeys(['up']):
        if image_1.pos[1] + image_1.size[1]/2 + image_1_step_size < screen_height/2:
            image_1.pos = (image_1.pos[0], image_1.pos[1] + image_1_step_size)
    elif event.getKeys(['down']):
        if image_1.pos[1] - image_1.size[1]/2 - image_1_step_size > -screen_height/2:
            image_1.pos = (image_1.pos[0], image_1.pos[1] - image_1_step_size)
    elif event.getKeys(['a']):
        image_2.pos = (image_2.pos[0] - image_2_step_size, image_2.pos[1])
    elif event.getKeys(['d']):
        image_2.pos = (image_2.pos[0] + image_2_step_size, image_2.pos[1])
    elif event.getKeys(['w']):
        image_2.pos = (image_2.pos[0], image_2.pos[1] + image_2_step_size)
    elif event.getKeys(['s']):
        image_2.pos = (image_2.pos[0], image_2.pos[1] - image_2_step_size)
    elif event.getKeys(['space']):
        if (xDist, yDist) in collision_space:
            collision_space.remove((xDist, yDist))
            defining_collision = False
        else:
            defining_collision = True  
    elif event.getKeys(['q']):
        break

    label.setText("X/Y dist: %d, %d" % (xDist, yDist))
    win.flip()

image_1.autoDraw = False
image_2.autoDraw = False


collision_space_by_y_prelim = {}
for x, y in collision_space:
    if y in collision_space_by_y_prelim:
        collision_space_by_y_prelim[y].append(x)
    else:
        collision_space_by_y_prelim[y] = [x]

collision_space_by_y = {}
for y_coord, x_coords in sorted(collision_space_by_y_prelim.items()):
    collision_space_by_y[y_coord] = (min(x_coords), max(x_coords))

if existing_map_file and starting_collision_space_by_y == collision_space_by_y:
    print "No changes were made to the collision space defined by the pre-loaded collision map file, so no new collision map file was created."
elif len(collision_space_by_y) > 0:
    f = open(output_file, 'w')
    pickle.dump(collision_space_by_y, f)
    print "A collision map for %s and %s was saved to %s." % (image_1_file, image_2_file, output_file)
else:
    print "No collision area was defined, so no collision map was created."

win.close()
core.quit()
