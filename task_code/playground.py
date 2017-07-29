#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.2),
    on Sat Jul 29 17:00:16 2017
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'playground'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'test'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/Jeff/sc_magic/psyexp/playground.psyexp',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "test_magic"
test_magicClock = core.Clock()
from optparse import OptionParser
from subprocess import Popen
import re


# immediately reset the frame duration to a smoother value
ideal_fps = 40.0
psychopy_calculated_fps = round(expInfo['frameRate'])
if psychopy_calculated_fps < ideal_fps:
    print "Warning: Psychopy internally calculated a frame rate of %f fps." % psychopy_calculated_fps
    print "The system might be having trouble maintaining the necessary framerate (%f fps)." % ideal_fps
frameDur = 1.0 / ideal_fps # frameDur is the internal value that determines game speed

# collect runtime options (can be supplied via command line, or the wrapper script can do it automatically)
parser = OptionParser()
parser.add_option("-s", "--source", metavar="SOURCE_DIR", dest="source_dir", help="the local sc task directory")
(options, args) = parser.parse_args()
project_dir = options.source_dir
if not project_dir:
    cwd = os.getcwd()
    project_dir = os.path.abspath("%s/.." % cwd)
    print "Project source not indicated with \"-s\" option, so guessing that it's %s..." % project_dir

if not project_dir:
    parser.print_help()
    core.quit()

if not os.access(project_dir, os.R_OK):
    print "Error: The specified project directory (%s) is either invalid or not readable." % project_dir
    sys.exit()


# folder that holds images and sounds used in the experiment
media = project_dir + "/sc_media/"

# distance wand moves per step (in pixels)
wand_step_size = 80

# screen size (these values just reflect what is already set by Psychopy)
screen_width = 1440
screen_height = 900


balloonImage = media + "pink_balloon.png"
magic_opacity = 0
magic_showing = False

left_key = 'left'
right_key = 'right'
up_key = 'up'
down_key = 'down'
avoid_background = visual.ImageStim(
    win=win, name='avoid_background',units='pix', 
    image=media + "Avoidance_period_background.jpg", mask=None,
    ori=0, pos=(0, 0), size=(screen_width, screen_height),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
balloon = visual.ImageStim(
    win=win, name='balloon',units='pix', 
    image=balloonImage, mask=None,
    ori=45, pos=[0,0], size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
wand = visual.ImageStim(
    win=win, name='wand',units='pix', 
    image=media + "magic_wand.png", mask=None,
    ori=0, pos=[0,0], size=(80, 70),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
magic = visual.ImageStim(
    win=win, name='magic',units='pix', 
    image=media + "magic-effect.png", mask=None,
    ori=0, pos=[0,0], size=(150, 150),
    color=[1,1,1], colorSpace='rgb', opacity=1.0,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
label_background = visual.ImageStim(
    win=win, name='label_background',units='pix', 
    image=media + "label_background.png", mask=None,
    ori=0, pos=(550, -435), size=(175, 45),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
label = visual.TextStim(win=win, name='label',
    text=None,
    font='Arial',
    units='pix', pos=(550, -432), height=24, wrapWidth=None, ori=0, 
    color='#053270', colorSpace='rgb', opacity=1,
    depth=-6.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "test_magic"-------
t = 0
test_magicClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
wand_position = (0, -.8 * screen_height/2)
balloon_pos = (0, 0)
# keep track of which components have finished
test_magicComponents = [avoid_background, balloon, wand, magic, label_background, label]
for thisComponent in test_magicComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "test_magic"-------
while continueRoutine:
    # get current time
    t = test_magicClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    new_wand_position = wand_position
    if event.getKeys([right_key]):
        if wand_position[0] + wand.size[0]/2 + wand_step_size < screen_width/2:
            new_wand_position = (wand_position[0] + wand_step_size, wand_position[1])
    elif event.getKeys([left_key]):
        if wand_position[0] - wand.size[0]/2 - wand_step_size > -screen_width/2: 
            new_wand_position = (wand_position[0] - wand_step_size, wand_position[1])
    elif event.getKeys([up_key]):
        if wand_position[1] + wand.size[1]/2 + wand_step_size < screen_height/2:
            new_wand_position = (wand_position[0], wand_position[1] + wand_step_size)
    elif event.getKeys([down_key]):
        if wand_position[1] - wand.size[1]/2 - wand_step_size > -screen_height/2:
            new_wand_position = (wand_position[0], wand_position[1] - wand_step_size)
    if wand_position != new_wand_position:
        wand_position = new_wand_position
    
    if event.getKeys(['a']):
        balloon_pos = (balloon.pos[0] - 1, balloon.pos[1])
    elif event.getKeys(['d']):
        balloon_pos = (balloon.pos[0] + 1, balloon.pos[1])
    elif event.getKeys(['w']):
        balloon_pos = (balloon.pos[0], balloon.pos[1] + 1)
    elif event.getKeys(['s']):
        balloon_pos = (balloon.pos[0], balloon.pos[1] - 1)
    
    # testing if the wand has reached the balloon
    xDist = abs(wand.pos[0] - balloon.pos[0])
    yDist = abs(wand.pos[1] - balloon.pos[1])
    label.setText("%d, %d" % (int(xDist), int(yDist)))
    
    if wand.overlaps(balloon):
        if not magic_showing:
            magic_opacity = .75
            magic_showing = True
    elif magic_showing:
        magic_opacity = 0
        magic_showing = False
    
    # *avoid_background* updates
    if t >= 0 and avoid_background.status == NOT_STARTED:
        # keep track of start time/frame for later
        avoid_background.tStart = t
        avoid_background.frameNStart = frameN  # exact frame index
        avoid_background.setAutoDraw(True)
    
    # *balloon* updates
    if t >= 0 and balloon.status == NOT_STARTED:
        # keep track of start time/frame for later
        balloon.tStart = t
        balloon.frameNStart = frameN  # exact frame index
        balloon.setAutoDraw(True)
    if balloon.status == STARTED:  # only update if drawing
        balloon.setPos(balloon_pos, log=False)
        balloon.setSize((120, 150), log=False)
    
    # *wand* updates
    if t >= 0 and wand.status == NOT_STARTED:
        # keep track of start time/frame for later
        wand.tStart = t
        wand.frameNStart = frameN  # exact frame index
        wand.setAutoDraw(True)
    if wand.status == STARTED:  # only update if drawing
        wand.setPos(wand_position, log=False)
    
    # *magic* updates
    if t >= 0 and magic.status == NOT_STARTED:
        # keep track of start time/frame for later
        magic.tStart = t
        magic.frameNStart = frameN  # exact frame index
        magic.setAutoDraw(True)
    if magic.status == STARTED:  # only update if drawing
        magic.setOpacity(magic_opacity, log=False)
        magic.setPos((balloon.pos[0] + 20, balloon.pos[1] + 50), log=False)
    
    # *label_background* updates
    if t >= 0.0 and label_background.status == NOT_STARTED:
        # keep track of start time/frame for later
        label_background.tStart = t
        label_background.frameNStart = frameN  # exact frame index
        label_background.setAutoDraw(True)
    
    # *label* updates
    if t >= 0.0 and label.status == NOT_STARTED:
        # keep track of start time/frame for later
        label.tStart = t
        label.frameNStart = frameN  # exact frame index
        label.setAutoDraw(True)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in test_magicComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "test_magic"-------
for thisComponent in test_magicComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "test_magic" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
