#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.85.2),
    on Wed Jul  5 09:04:09 2017
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
expName = 'balloon_game'  # from the Builder filename that created this script
expInfo = {u'dont_use': u''}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + "BalloonGame_%s" % expInfo['date']

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/Jeff/sc_magic/psyexp/BalloonGame.psyexp',
    savePickle=True, saveWideText=False,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1440, 900), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='norm')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "initialize"
initializeClock = core.Clock()
from optparse import OptionParser, SUPPRESS_HELP
from datetime import datetime
from subprocess import Popen, call

# collect runtime options (can be supplied via command line, or the wrapper script can do it automatically)
parser = OptionParser()
parser.add_option("-s", "--source", metavar="SOURCE_DIR", dest="source_dir", help="the local sc task directory")
parser.add_option("-i", "--id", metavar="ID", dest="id", help="the participant ID")
parser.add_option("-o", "--output", metavar="OUTPUT_DIR", dest="output_dir", help="the directory where output/logs should be saved")
parser.add_option("-y", "--yoke_source", metavar="YOKE_SOURCE", dest="yoke_source", help="a yoking file to which the current participant should be yoked")
parser.add_option("-b", "--boring_mode", action="store_true", dest="is_boring", help="invokes non-stress version of game")
parser.add_option("-B", "--button_box", action="store_true", default=False, dest="button_box_mode", help="use button box input (1-4 instead of right, down, left, up)")
parser.add_option("-v", "--version", metavar="VERSION", dest="version", help=SUPPRESS_HELP, default="unknown")
(options, args) = parser.parse_args()
projectDir = options.source_dir
outputDir = options.output_dir
id = options.id
yokeSourceFile = options.yoke_source
boringMode = options.is_boring
version = options.version
button_box_mode = options.button_box_mode

if button_box_mode:
    right_key = "1"
    down_key = "2"
    left_key = "3"
    up_key = "4"
else:
    right_key = "right"
    down_key = "down"
    left_key = "left"
    up_key = "up"

if not projectDir or not outputDir or not id:
    parser.print_help()
    Popen("sleep 5; rm %s.log %s.psydat" %(filename, filename), shell=True)
    sys.exit()

logDir = outputDir + "/logs"
if not os.path.exists(logDir): os.mkdir(logDir)

new_filename = "%s/BalloonGame_%s_%s" % (logDir, id, expInfo['date'])
call("mv %s* %s.log" % (filename, new_filename), shell=True)
filename = new_filename

# set variable to "controllable_stress", "uncontrollable_stress", or "nonstressed"
condition = "unknown"
if boringMode:
    condition = "nonstressed"
elif yokeSourceFile:
    condition = "uncontrollable_stress"
else:
    condition = "controllable_stress"


# folder that holds images and sounds used in the experiment
media = projectDir + "/sc_media/"
instructionSlides = media + "Balloon_instruction_slides/"
boringInstructionSlides = media + "Balloon_nonstressed_instruction_slides/"

# setting up where to store output data
outputFile = "%s/BalloonGame_%s_%s_data.txt" % (outputDir, id, expInfo['date'])
f = open(outputFile, 'w')

# setting up for unyoked participants (uncontrollable stress)
yokingOutputDir = outputDir + "/yoking_files"
isYokedParticipant = False
if yokeSourceFile:
    isYokedParticipant = True
    try:
        y = open(yokeSourceFile, 'r')
    except:
        print "Error: Could not open yoke source file %s" % yokeSourceFile
        core.quit()
else:
    yokingOutputFile = "%s/BalloonGame_%s_%s_yoke.txt" % (yokingOutputDir, id, expInfo['date'])
    try:
        y = open(yokingOutputFile, 'w')
    except:
        print "Error: Could not create yoking file %s" % yokingOutputFile
        core.quit()

# turn on the non-stressed mode, if applicable
if (boringMode and not isYokedParticipant):
    print "Error: Non-stressed (boring) condition was selected without a yoking source file being specified."
    core.quit()


# length of anticipatory period (before each trial starts)
anticipatoryPeriod = 4

# length of time between trials (for MRI synching)
itiLength = 10

# allowing a mode for debugging specific trials
trialDebugMode = False
debugTrial = 0
for i in range(1, 31): # that's python for 1-30!
    if id == ("test" + str(i)):
        trialDebugMode = True
        debugTrial = i
        itiLength = 1

# allowing a test mode with shortened waiting periods
if id == "test":
    itiLength = 1


# Initialize components for Routine "game_instr"
game_instrClock = core.Clock()

slides = visual.ImageStim(
    win=win, name='slides',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "boring_instr"
boring_instrClock = core.Clock()

instruction = visual.ImageStim(
    win=win, name='instruction',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "wand_practice"
wand_practiceClock = core.Clock()
wand_position = (0, 0)

magic_wand = visual.ImageStim(
    win=win, name='magic_wand',units='norm', 
    image=media + "magic_wand.png", mask=None,
    ori=0, pos=[0,0], size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
time_left = visual.TextStim(win=win, name='time_left',
    text=None,
    font='Arial',
    units='norm', pos=(.9, -.8), height=0.1, wrapWidth=None, ori=0, 
    color='#053270', colorSpace='rgb', opacity=1,
    depth=-2.0);

# Initialize components for Routine "get_ready"
get_readyClock = core.Clock()
InstructSlide14 = visual.ImageStim(
    win=win, name='InstructSlide14',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)


# Initialize components for Routine "balloons"
balloonsClock = core.Clock()


# signals when the user has successfully halted the balloon
success = 0

# time when trial ends (regardless of catching balloon)
endTrialTime = anticipatoryPeriod + 4.5

# will be used to keep track of time after halting balloon
successClock = core.Clock()

# set balloon speed (x direction)
xSpeed1 = .008
xSpeed2 = .009
xSpeed3 = .01
xSpeed4 = -.008
xSpeed5 = -.009
xSpeed6 = -.01

# set balloon speed (y direction)
ySpeed1 = .01
ySpeed2 = .01
ySpeed3 = .01


# different balloon starting X/Y positions and per-frame X/Y movements
balloonSettings = [(.4, -1, xSpeed6, ySpeed1, [-.8, .8, -.8, .8, -.8, .8, -.8]), 
(.8, -1, xSpeed4, ySpeed1, [0, .7, -.2, .3, -.7, .7, -.8]),
(-.7, -1, xSpeed2, ySpeed2, [0, -.5, .9, -.6, .7, -.5]), 
(-.4, -1, xSpeed2, ySpeed2, [.8, -.8, .8, -.8, 0, -.5]),
(-.6, -1, xSpeed2, ySpeed3, [-.2, -.8, -.6, -.8, -.3, -.5, -.2]), 
(.7, -1, xSpeed4, ySpeed1, [-.8, .8, -.8, -.4, -.6, 0, -.3, .8, -.8]), 
(.1,-1, xSpeed2,ySpeed3, [.7, -.7, .7, 0, -.2, .3, -.7, .7, -.7]), 
(-.3, -1, xSpeed2, ySpeed2, [0, -.8, .6, -.8, .6]),     
(.9, -1, xSpeed6, ySpeed2, [0, .9, .3, .5, -.2,.8]),
(-.8, -1, xSpeed1, ySpeed1, [-.3, -.7, -.2, -.8, -.1]), 
(.4, -1, xSpeed4, ySpeed2, [0, .8, -.3, .3, -.7, .8, -.6, 0]),
(.5, -1, xSpeed6, ySpeed2, [0, .7, -.8, .8, 0, .5, -.5, .5, -.1]), 
(.5, -1, xSpeed4, ySpeed1, [0, .8, .1, -.1, 0, -.3, .3, -.5, .8]), 
(-.6, -1, xSpeed3, ySpeed1, [0, -.5, .9, -.7, .7, -.6]),     
(-.9, -1, xSpeed2, ySpeed3, [0, -.2, .3, -.4, .3, -.5, .7, -.8]), # 15
(-.5, -1, xSpeed3, ySpeed1, [0, -.4, .3, -.1, .1, -.3, .4, -.5, .5, -.6, .6, -.7]), 
(.3, -1, xSpeed5, ySpeed3, [0, .7, -.2, .3, -.6, .7, -.8]),     
(.2,-1, xSpeed3,ySpeed1, [.4, .2, .8, .1, .8, .4, .6]),
(-.3,-1, xSpeed2, ySpeed1, [-.2, -.7, .3, 0, .1, -.3, .3, -.5, .7]),     
(-.5, -1, xSpeed1, ySpeed2, [-.1, -.2, .2, -.4, .4,-.7]), 
(.8, -1, xSpeed4, ySpeed1, [0, .7, -.2, .3, -.7, .7, -.8]),
(-.7, -1, xSpeed2, ySpeed2, [0, -.5, .9, -.6, .7, -.5]), 
(-.4, -1, xSpeed2, ySpeed2, [.8, -.8, .8, -.8, 0, -.5]),
(-.6, -1, xSpeed2, ySpeed3, [-.2, -.8, -.6, -.8, -.3, -.5, -.2]), 
(.7, -1, xSpeed4, ySpeed1, [-.8, .8, -.8, -.4, -.6, 0, -.3, .8, -.8]), 
(.5,-1, xSpeed2,ySpeed3, [.7, -.7, .7, 0, -.2, .3, -.7, .7, -.7]), 
(-.8, -1, xSpeed1, ySpeed1, [-.3, -.7, -.2, -.8, -.1]), 
(.4, -1, xSpeed4, ySpeed2, [0, .8, -.3, .3, -.7, .8, -.6, 0]),
(.8, -1, xSpeed6, ySpeed2, [0, .7, -.8, .8, 0, .5, -.5, .5, -.1]), 
(.5, -1, xSpeed4, ySpeed1, [0, .8, .1, -.1, 0, -.3, .3, -.5, .8]), 
(-.6, -1, xSpeed3, ySpeed1, [0, -.5, .9, -.7, .7, -.6]), 
(-.2, -1, xSpeed1, ySpeed2, [0, -.2, .2, -.4, .4,-.7]),     
(-.5, -1, xSpeed3, ySpeed1, [0, -.4, .3, -.1, .1, -.3, .4, -.5, .5, -.6, .6, -.7]), 
(-.3, -1, xSpeed2, ySpeed2, [0, -.8, .6, -.8, .6]),  
(.2, -1, xSpeed5, ySpeed3, [0, .7, -.2, .3, -.6, .7, -.8]),     
(.2,-1, xSpeed3,ySpeed1, [.4, .2, .8, .1, .8, .4, .6]),
(.9, -1, xSpeed6, ySpeed2, [0, .9, .3, .5, -.2,.8]),
(-.9, -1, xSpeed2, ySpeed3, [0, -.2, .3, -.4, .3, -.5, .7, -.8]), 
(-.3,-1, xSpeed2, ySpeed1, [-.2, -.7, .3, 0, .1, -.3, .3, -.5, .7])]

# log info
currentTrial = 0
totalPopped = 0
totalSaved = 0

# write data file headers
f.write("# Version: %s\n" % version)
f.write("# Condition: %s\n" % condition)
if condition != "controllable_stress":
    f.write("# Yoked to: %s\n" % yokeSourceFile)
f.write("ID\tTime\tTrial\tRel_time\tX_balloon\tY_balloon\tX_wand\tY_wand\tkey_just_pressed\tvalid_key_press\t" +
"total_key_presses\ttotal_valid_key_presses\tjust_popped_balloon\tjust_saved_balloon\ttotal_popped\ttotal_saved\n")

# write yoking file headers
if (not isYokedParticipant):
    y.write("ID\tTrial\tBalloon_saved\tSuccess_time\n")
else:
    y.readline() # skip header line
    previousParticipantOutcomes = y.readlines()
    if len(previousParticipantOutcomes) != 30:
        print "Error: Yoking file " + yokeSourceFile + " doesn't appear to have one line per trial."
        core.quit()

# volume of aversive pop (gets changed to 0 in nonstressed condition)
popVolume = 1

antic_background = visual.ImageStim(
    win=win, name='antic_background',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
avoid_background = visual.ImageStim(
    win=win, name='avoid_background',units='norm', 
    image=media + "Avoidance_period_background.jpg", mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
success_background = visual.ImageStim(
    win=win, name='success_background',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
balloon = visual.ImageStim(
    win=win, name='balloon',units='norm', 
    image='sin', mask=None,
    ori=45, pos=[0,0], size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
wand = visual.ImageStim(
    win=win, name='wand',units='norm', 
    image=media + "magic_wand.png", mask=None,
    ori=0, pos=[0,0], size=(0.2, 0.2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-5.0)
aversive_pop = sound.Sound(media + "Balloon_Pop.wav", secs=-1)
aversive_pop.setVolume(1.0)
ITI = visual.ImageStim(
    win=win, name='ITI',units='norm', 
    image=media + "iti_background.jpg", mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-7.0)

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
Thankyo = visual.ImageStim(
    win=win, name='Thankyo',
    image=instructionSlides + "Slide19.jpg", mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "initialize"-------
t = 0
initializeClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat

# keep track of which components have finished
initializeComponents = []
for thisComponent in initializeComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "initialize"-------
while continueRoutine:
    # get current time
    t = initializeClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in initializeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "initialize"-------
for thisComponent in initializeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "initialize" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "game_instr"-------
t = 0
game_instrClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
currentInstructionNumber = 1

if trialDebugMode or boringMode:
    continueRoutine = False


get_key_press = event.BuilderKeyResponse()
# keep track of which components have finished
game_instrComponents = [get_key_press, slides]
for thisComponent in game_instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "game_instr"-------
while continueRoutine:
    # get current time
    t = game_instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # all slides advance with a space, except slides 9, 10, 11, 12 (arrow key slides)
    if event.getKeys('space') and (currentInstructionNumber < 9 or currentInstructionNumber > 12):
        currentInstructionNumber += 1
    if event.getKeys('left') and currentInstructionNumber == 9:
        currentInstructionNumber += 1
    if event.getKeys('right') and currentInstructionNumber == 10:
        currentInstructionNumber += 1
    if event.getKeys('down') and currentInstructionNumber == 11:
        currentInstructionNumber += 1
    if event.getKeys('up') and currentInstructionNumber == 12:
        currentInstructionNumber += 1
    
    if currentInstructionNumber == 14:
        continueRoutine = False
    
    currentInstructionString = str(currentInstructionNumber)
    if currentInstructionNumber < 10:
        currentInstructionString = "0" + currentInstructionString
    currentInstructionFile = instructionSlides + "Slide" + currentInstructionString + ".jpg"
    
    
    
    # *get_key_press* updates
    if t >= 0 and get_key_press.status == NOT_STARTED:
        # keep track of start time/frame for later
        get_key_press.tStart = t
        get_key_press.frameNStart = frameN  # exact frame index
        get_key_press.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(get_key_press.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if get_key_press.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys) > 0:  # at least one key was pressed
            get_key_press.keys = theseKeys[-1]  # just the last key pressed
            get_key_press.rt = get_key_press.clock.getTime()
    
    # *slides* updates
    if t >= 0.0 and slides.status == NOT_STARTED:
        # keep track of start time/frame for later
        slides.tStart = t
        slides.frameNStart = frameN  # exact frame index
        slides.setAutoDraw(True)
    if slides.status == STARTED:  # only update if drawing
        slides.setImage(currentInstructionFile, log=False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in game_instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "game_instr"-------
for thisComponent in game_instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if get_key_press.keys in ['', [], None]:  # No response was made
    get_key_press.keys=None
thisExp.addData('get_key_press.keys',get_key_press.keys)
if get_key_press.keys != None:  # we had a response
    thisExp.addData('get_key_press.rt', get_key_press.rt)
thisExp.nextEntry()
# the Routine "game_instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "boring_instr"-------
t = 0
boring_instrClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
currentInstructionNumber = 1
if trialDebugMode or not boringMode:
    continueRoutine = False
# keep track of which components have finished
boring_instrComponents = [instruction]
for thisComponent in boring_instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "boring_instr"-------
while continueRoutine:
    # get current time
    t = boring_instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # all slides advance with a space
    if event.getKeys('space'):
        currentInstructionNumber += 1
    
    if currentInstructionNumber == 11:
        break
    
    currentInstructionString = str(currentInstructionNumber)
    if currentInstructionNumber < 10:
        currentInstructionString = "0" + currentInstructionString
    currentInstructionFile = boringInstructionSlides + "Slide" + currentInstructionString + ".jpg"
    
    
    # *instruction* updates
    if t >= 0.0 and instruction.status == NOT_STARTED:
        # keep track of start time/frame for later
        instruction.tStart = t
        instruction.frameNStart = frameN  # exact frame index
        instruction.setAutoDraw(True)
    if instruction.status == STARTED:  # only update if drawing
        instruction.setImage(currentInstructionFile, log=False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in boring_instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "boring_instr"-------
for thisComponent in boring_instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "boring_instr" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "wand_practice"-------
t = 0
wand_practiceClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(20.000000)
# update component parameters for each repeat
if trialDebugMode or boringMode:
    continueRoutine = False

practice_length = 20.0
rounded_seconds_remaining = practice_length
time_left.setText(str(int(rounded_seconds_remaining)))

# keep track of which components have finished
wand_practiceComponents = [magic_wand, time_left]
for thisComponent in wand_practiceComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "wand_practice"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = wand_practiceClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # moving wand when arrow keys are clicked during the main part of the trial
    new_wand_position = wand_position
    if event.getKeys([right_key]):
        if wand_position[0] < .8:
            new_wand_position = (wand_position[0] + .1, wand_position[1])
    if event.getKeys([left_key]):
        if wand_position[0] > -.8: 
            new_wand_position = (wand_position[0] - .1, wand_position[1])
    if event.getKeys([up_key]):
        if wand_position[1] < .8:
            new_wand_position = (wand_position[0], wand_position[1] + .1)
    if event.getKeys([down_key]):
        if wand_position[1] > -.8:
            new_wand_position = (wand_position[0], wand_position[1] - .1)
    
    # moving wand unless it would cover the counter
    rounded_pos = (round(new_wand_position[0], 1), round(new_wand_position[1], 1))
    if rounded_pos != (.9, -.8):   
        wand_position = new_wand_position
    
    seconds_remaining = practice_length - t
    if seconds_remaining < rounded_seconds_remaining - 1:
        rounded_seconds_remaining -= 1
        time_left.setText(str(int(rounded_seconds_remaining)))
    
    if event.getKeys("escape"):
        continueRoutine=False
    
    # *magic_wand* updates
    if t >= 0 and magic_wand.status == NOT_STARTED:
        # keep track of start time/frame for later
        magic_wand.tStart = t
        magic_wand.frameNStart = frameN  # exact frame index
        magic_wand.setAutoDraw(True)
    frameRemains = 0 + 20- win.monitorFramePeriod * 0.75  # most of one frame period left
    if magic_wand.status == STARTED and t >= frameRemains:
        magic_wand.setAutoDraw(False)
    if magic_wand.status == STARTED:  # only update if drawing
        magic_wand.setPos(wand_position, log=False)
    
    # *time_left* updates
    if t >= 0.0 and time_left.status == NOT_STARTED:
        # keep track of start time/frame for later
        time_left.tStart = t
        time_left.frameNStart = frameN  # exact frame index
        time_left.setAutoDraw(True)
    frameRemains = 0.0 + 20- win.monitorFramePeriod * 0.75  # most of one frame period left
    if time_left.status == STARTED and t >= frameRemains:
        time_left.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in wand_practiceComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "wand_practice"-------
for thisComponent in wand_practiceComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


# ------Prepare to start Routine "get_ready"-------
t = 0
get_readyClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
currentInstructionNumber = 14

if trialDebugMode or boringMode:
    continueRoutine = False

# keep track of which components have finished
get_readyComponents = [InstructSlide14]
for thisComponent in get_readyComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "get_ready"-------
while continueRoutine:
    # get current time
    t = get_readyClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *InstructSlide14* updates
    if t >= 0.0 and InstructSlide14.status == NOT_STARTED:
        # keep track of start time/frame for later
        InstructSlide14.tStart = t
        InstructSlide14.frameNStart = frameN  # exact frame index
        InstructSlide14.setAutoDraw(True)
    if InstructSlide14.status == STARTED:  # only update if drawing
        InstructSlide14.setImage(currentInstructionFile, log=False)
    # all slides advance with a space
    if event.getKeys('space') and currentInstructionNumber != 18:
        currentInstructionNumber += 1
    
    if event.getKeys('right') and currentInstructionNumber == 18:
        currentInstructionNumber +=1
    
    if currentInstructionNumber == 19:
        break
    
    currentInstructionString = str(currentInstructionNumber)
    if currentInstructionNumber < 10:
        currentInstructionString = "0" + currentInstructionString
    currentInstructionFile = instructionSlides + "Slide" + currentInstructionString + ".jpg"
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in get_readyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "get_ready"-------
for thisComponent in get_readyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "get_ready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=30, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    # ------Prepare to start Routine "balloons"-------
    t = 0
    balloonsClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # indicator variable to track if it's time to pop the balloon
    timeToPop = 0
    success = 0
    startedTrial = 0
    timeSinceSuccess = 0
    
    wand_position = (0, -.8)
    balloonImage = media + "pink_balloon.png"
    currentBalloonSettings = balloonSettings.pop(0)
    balloonPosition = (currentBalloonSettings[0], currentBalloonSettings[1])
    print str(currentTrial) + "\t" + str(balloonPosition)
    balloonShift = (currentBalloonSettings[2], currentBalloonSettings[3])
    zigs = currentBalloonSettings[4]
    
    if boringMode:
        popVolume = 0
    
    if isYokedParticipant:
        trialInfo = previousParticipantOutcomes.pop(0).rstrip().split("\t")
        print "Using this line from yoke source file: " + "\t".join(trialInfo)
        balloonToBeSaved = False
        if trialInfo[-2] == "1":
            balloonToBeSaved = True
            safetySignalTime = float(trialInfo[-1])
    
    # log info
    currentTrial += 1
    totalKeyPresses = 0
    totalValidKeyPresses = 0
    justPoppedBalloon = 0
    justSavedBalloon = 0
    updateLog = 0
    
    if trialDebugMode:
        if currentTrial != debugTrial:
            print "This trial is " + str(currentTrial) + ", debug trial is " + str(debugTrial)
            continue
    
    antic_background.setImage(media + "Anticipatory_period_background.jpg")
    success_background.setImage(media + "Success_background.jpg")
    aversive_pop.setVolume(popVolume)
    # keep track of which components have finished
    balloonsComponents = [antic_background, avoid_background, success_background, balloon, wand, aversive_pop, ITI]
    for thisComponent in balloonsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "balloons"-------
    while continueRoutine:
        # get current time
        t = balloonsClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # initializing defaults for logs
        keyJustPressed = '0'
        validKeyPress = 'NA'
        
        
        # moving wand when arrow keys are clicked during the main part of the trial
        # in controllable stress condition, wand freezes when balloon is saved (success), but not in uncontrollable condition
        if startedTrial and (not success or isYokedParticipant) and not timeToPop:
            if event.getKeys([right_key]):
                updateLog = 1
                keyJustPressed = 'right'
                totalKeyPresses += 1
                validKeyPress = '0'
                if wand_position[0] < .8:
                    wand_position = (wand_position[0] + .1, wand_position[1])
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([left_key]):
                updateLog = 1
                keyJustPressed = 'left'
                totalKeyPresses += 1
                validKeyPress = '0'
                if wand_position[0] > -.8:
                    wand_position = (wand_position[0] - .1, wand_position[1])
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([up_key]):
                updateLog = 1
                keyJustPressed = 'up'
                totalKeyPresses += 1
                validKeyPress = '0'
                if wand_position[1] < .8:
                    wand_position = (wand_position[0], wand_position[1] + .1)
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([down_key]):
                updateLog = 1
                keyJustPressed = 'down'
                totalKeyPresses += 1
                validKeyPress = '0'
                if wand_position[1] > -.8:
                    wand_position = (wand_position[0], wand_position[1] - .1)
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            else:
                keyJustPressed = ''.join(event.getKeys())
                if keyJustPressed != '':
                    updateLog = 1
                    validKeyPress = '0'
                    totalKeyPresses += 1
        
        
        # moving the balloon during the main part of the trial
        if (not success or isYokedParticipant) and not timeToPop and startedTrial:
            balloonPosition = (balloon.pos[0] + balloonShift[0], balloon.pos[1] + balloonShift[1]) # starting just off screen
            if len(zigs) > 0:
                if abs(balloon.pos[0] - zigs[0]) < .01:
                    balloonShift = (-balloonShift[0], balloonShift[1])
                    zigs.pop(0)
        
        # signaling when the main part of the trial has started
        if t > anticipatoryPeriod:
            startedTrial = 1
        
        
        # testing if the wand has reached the balloon (for controllable stress condition) or if it's time for a yoked participant to be saved
        xDist = abs(wand.pos[0] - balloon.pos[0])
        yDist = abs(wand.pos[1] - balloon.pos[1])
        
        # if balloon reaches top, balloon will pop (so don't need the success component)
        if balloon.pos[1] > .85 and success == 0:
            success_background.status = FINISHED
            if timeToPop == 0:
                justPoppedBalloon = 1
                totalPopped += 1
                balloonImage = media + "pop_1.png"
                updateLog = 1
                if not isYokedParticipant:
                    yokingParams = [id, str(currentTrial), "0", "NA"] # 0 means balloon not saved (and saving time is NA)
                    y.write("\t".join(yokingParams + ["\n"]))
            else:
                justPoppedBalloon = 0
                core.wait(.2)
                balloonImage = media + "pop_2.png"
            timeToPop = 1
        elif ((t > anticipatoryPeriod + .1 and xDist < .05 and yDist < .05 and not isYokedParticipant) or (isYokedParticipant and balloonToBeSaved and t >= safetySignalTime)):
            # note that you need the .1 second buffer so the wand is initialized before the test
            if success == 0:
                successClock.reset()
                justSavedBalloon = 1
                totalSaved += 1
                updateLog = 1
                if not isYokedParticipant:
                    yokingParams = [id, str(currentTrial), str(justSavedBalloon), str(t)]
                    y.write("\t".join(yokingParams + ["\n"]))
            else:
                justSavedBalloon = 0
            success = 1
            aversive_pop.status = FINISHED
        
        if (success):
            timeSinceSuccess = successClock.getTime()
        
        # logging
        logInfo = [id, str(datetime.now()), str(currentTrial), str(t), str(balloon.pos[0]), str(balloon.pos[1]), 
            str(wand.pos[0]), str(wand.pos[1]), keyJustPressed, validKeyPress, str(totalKeyPresses), str(totalValidKeyPresses), 
            str(justPoppedBalloon), str(justSavedBalloon), str(totalPopped), str(totalSaved)]
        
        if updateLog == 1:
            f.write("\t".join(logInfo + ["\n"]))
            updateLog = 0
        
        # *antic_background* updates
        if t >= 0.0 and antic_background.status == NOT_STARTED:
            # keep track of start time/frame for later
            antic_background.tStart = t
            antic_background.frameNStart = frameN  # exact frame index
            antic_background.setAutoDraw(True)
        frameRemains = 0.0 + anticipatoryPeriod- win.monitorFramePeriod * 0.75  # most of one frame period left
        if antic_background.status == STARTED and t >= frameRemains:
            antic_background.setAutoDraw(False)
        
        # *avoid_background* updates
        if (t >= anticipatoryPeriod) and avoid_background.status == NOT_STARTED:
            # keep track of start time/frame for later
            avoid_background.tStart = t
            avoid_background.frameNStart = frameN  # exact frame index
            avoid_background.setAutoDraw(True)
        if avoid_background.status == STARTED and bool(success==1 or t>=endTrialTime):
            avoid_background.setAutoDraw(False)
        
        # *success_background* updates
        if (success==1) and success_background.status == NOT_STARTED:
            # keep track of start time/frame for later
            success_background.tStart = t
            success_background.frameNStart = frameN  # exact frame index
            success_background.setAutoDraw(True)
        if success_background.status == STARTED and bool(t>=endTrialTime):
            success_background.setAutoDraw(False)
        
        # *balloon* updates
        if t >= t>=anticipatoryPeriod and balloon.status == NOT_STARTED:
            # keep track of start time/frame for later
            balloon.tStart = t
            balloon.frameNStart = frameN  # exact frame index
            balloon.setAutoDraw(True)
        if balloon.status == STARTED and bool(t>=endTrialTime):
            balloon.setAutoDraw(False)
        if balloon.status == STARTED:  # only update if drawing
            balloon.setPos(balloonPosition, log=False)
            balloon.setImage(balloonImage, log=False)
            balloon.setSize((0.25, 0.25), log=False)
        
        # *wand* updates
        if t >= t>=anticipatoryPeriod and wand.status == NOT_STARTED:
            # keep track of start time/frame for later
            wand.tStart = t
            wand.frameNStart = frameN  # exact frame index
            wand.setAutoDraw(True)
        if wand.status == STARTED and bool(timeToPop or t>endTrialTime):
            wand.setAutoDraw(False)
        if wand.status == STARTED:  # only update if drawing
            wand.setPos(wand_position, log=False)
        # start/stop aversive_pop
        if (timeToPop and not success) and aversive_pop.status == NOT_STARTED:
            # keep track of start time/frame for later
            aversive_pop.tStart = t
            aversive_pop.frameNStart = frameN  # exact frame index
            aversive_pop.play()  # start the sound (it finishes automatically)
        
        # *ITI* updates
        if (t >= endTrialTime) and ITI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ITI.tStart = t
            ITI.frameNStart = frameN  # exact frame index
            ITI.setAutoDraw(True)
        if ITI.status == STARTED and t >= (ITI.tStart + itiLength):
            ITI.setAutoDraw(False)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in balloonsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "balloons"-------
    for thisComponent in balloonsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # to make clear that start of next routine in loop is not immediate victory
    balloon.pos[1] = 0
    aversive_pop.stop()  # ensure sound has stopped at end of routine
    # the Routine "balloons" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 30 repeats of 'trials'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_14 = event.BuilderKeyResponse()
# keep track of which components have finished
thanksComponents = [Thankyo, key_resp_14]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Thankyo* updates
    if t >= 0.0 and Thankyo.status == NOT_STARTED:
        # keep track of start time/frame for later
        Thankyo.tStart = t
        Thankyo.frameNStart = frameN  # exact frame index
        Thankyo.setAutoDraw(True)
    frameRemains = 0.0 + 3.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if Thankyo.status == STARTED and t >= frameRemains:
        Thankyo.setAutoDraw(False)
    
    # *key_resp_14* updates
    if t >= 0.0 and key_resp_14.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_14.tStart = t
        key_resp_14.frameNStart = frameN  # exact frame index
        key_resp_14.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_14.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_14.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_14.keys = theseKeys[-1]  # just the last key pressed
            key_resp_14.rt = key_resp_14.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in thanksComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "thanks"-------
for thisComponent in thanksComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# check responses
if key_resp_14.keys in ['', [], None]:  # No response was made
    key_resp_14.keys=None
thisExp.addData('key_resp_14.keys',key_resp_14.keys)
if key_resp_14.keys != None:  # we had a response
    thisExp.addData('key_resp_14.rt', key_resp_14.rt)
thisExp.nextEntry()
# the Routine "thanks" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()
print "Finished the game!"





f.close()
y.close()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
