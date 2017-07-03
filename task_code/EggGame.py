#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.2),
    on Mon Jul  3 14:52:53 2017
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
expName = 'EggGame'  # from the Builder filename that created this script
expInfo = {u'participantID': u'preselected'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + "EggGame_%s" % expInfo['date']

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/Jeff/sc_magic/psyexp/EggGame.psyexp',
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
from subprocess import Popen, call

# collect runtime options (can be supplied via command line, or the wrapper script can do it automatically)
parser = OptionParser()
parser.add_option("-s", "--source", metavar="SOURCE_DIR", dest="source_dir", help="the local sc task directory")
parser.add_option("-i", "--id", metavar="ID", dest="id", help="the participant ID")
parser.add_option("-o", "--output", metavar="OUTPUT_DIR", dest="output_dir", help="the directory where output/logs should be saved")
parser.add_option("-B", "--button_box", action="store_true", default=False, dest="button_box_mode", help="use button box input (1-4 instead of right, down, left, up)")
parser.add_option("-v", "--version", metavar="VERSION", dest="version", default="unknown", help=SUPPRESS_HELP)

(options, args) = parser.parse_args()
projectDir = options.source_dir
outputDir = options.output_dir
id = options.id
version= options.version
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
    Popen("sleep 5; rm %s.log %s.psydat" %(filename, filename), shell=True)
    parser.print_help()
    core.quit()

logDir = outputDir + '/logs'
if not os.path.exists(logDir): os.mkdir(logDir)

# Moving Psychopy's automatic log files to a better location
new_filename = "%s/NoiseRating_%s_%s" % (logDir, id, expInfo['date'])
call("mv %s* %s.log" % (filename, new_filename), shell=True)
filename = new_filename


media = projectDir + "/sc_media/"
instructionSlides = media + "Egg_instruction_slides/"

# import datetime 
from datetime import datetime


# define output file
outputFile = "%s/EggGame_%s_%s_data.txt" %(outputDir, id, expInfo['date'])


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

# Initialize components for Routine "instructions"
instructionsClock = core.Clock()

instruction = visual.ImageStim(
    win=win, name='instruction',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)

# Initialize components for Routine "Practicehand"
PracticehandClock = core.Clock()
handPosition = (0, 0)


theHand = visual.ImageStim(
    win=win, name='theHand',units='norm', 
    image=media + "hand.png", mask=None,
    ori=0, pos=[0,0], size=(0.15, 0.15),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)

# Initialize components for Routine "get_ready"
get_readyClock = core.Clock()
InstructSlide14 = visual.ImageStim(
    win=win, name='InstructSlide14',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)


# Initialize components for Routine "Eggs"
EggsClock = core.Clock()
# y speeds
ySpeed1 = -.009
ySpeed2 = -.008
ySpeed3 = -.007

# xSpeeds
xSpeed1 = 0
xSpeed2 = .002
xSpeed3 = .003
xSpeed4 = .005

# egg starting X positions and per-frame X/Y movements
eggSettings = [(0, xSpeed1, ySpeed2), (-.5, xSpeed3, ySpeed3), (.8, -xSpeed2, ySpeed3),
                (-.9, xSpeed3, ySpeed2), (-.5, xSpeed1, ySpeed1), (.9, -xSpeed4, ySpeed2),
                (.2, xSpeed2, ySpeed2), (-.8, xSpeed4, ySpeed1), (.1, xSpeed2, ySpeed1),
                (-.3, -xSpeed3, ySpeed2), (.7, -xSpeed2, ySpeed1), (.3, -xSpeed4, ySpeed3),
                (-.8, xSpeed1, ySpeed2), (-.7, xSpeed4, ySpeed1), (.1, -xSpeed3, ySpeed2), 
                (-.5, xSpeed3, ySpeed3), (.8, -xSpeed2, ySpeed3), (.9, -xSpeed4, ySpeed2),
                (-.9, xSpeed3, ySpeed2), (-.5, xSpeed1, ySpeed1), (.1, -xSpeed3, ySpeed2),
                (.2, xSpeed2, ySpeed2), (-.8, xSpeed4, ySpeed1), (0, xSpeed1, ySpeed2),
                (.1, xSpeed2, ySpeed1), (-.3, -xSpeed3, ySpeed2), (.7, -xSpeed2, ySpeed1), 
                (.3, -xSpeed4, ySpeed3), (-.8, xSpeed1, ySpeed2), (-.7, xSpeed4, ySpeed1)]
eggDegrees = 0

# log info
currentTrial = 0
f = open(outputFile, 'w')
f.write("# Version: %s\n" % version)
f.write("ID\tTime\tTrial\tRel_time\tX_egg\tY_egg\tX_hand\tY_hand\tkey_just_pressed\tvalid_key_press\t" +
"total_key_presses\ttotal_valid_key_presses\tjust_cracked_egg\n")


antic_background = visual.ImageStim(
    win=win, name='antic_background',units='norm', 
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2,2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
avoid_background = visual.ImageStim(
    win=win, name='avoid_background',units='norm', 
    image=media + "T2_Avoidance_background.jpg", mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
egg = visual.ImageStim(
    win=win, name='egg',units='norm', 
    image=media + "egg.png", mask=None,
    ori=1.0, pos=[0,0], size=1.0,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
the_hand = visual.ImageStim(
    win=win, name='the_hand',units='norm', 
    image=media + "hand.png", mask=None,
    ori=0, pos=[0,0], size=(0.1, 0.1),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
aversive_crack = sound.Sound(media + "egg_crack.wav", secs=-1)
aversive_crack.setVolume(1)
ITI = visual.ImageStim(
    win=win, name='ITI',units='norm', 
    image=media + "iti_background.jpg", mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-6.0)

# Initialize components for Routine "thanks"
thanksClock = core.Clock()
Thankyou = visual.ImageStim(
    win=win, name='Thankyou',
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

# ------Prepare to start Routine "instructions"-------
t = 0
instructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
currentInstructionNumber = 1

if trialDebugMode:
    continueRoutine = False
user_start_signal = event.BuilderKeyResponse()
# keep track of which components have finished
instructionsComponents = [user_start_signal, instruction]
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "instructions"-------
while continueRoutine:
    # get current time
    t = instructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # all slides advance with a space, except slides 9, 10, 11, 12 (arrow key slides)
    if event.getKeys('space') and (currentInstructionNumber < 8 or currentInstructionNumber > 11):
        currentInstructionNumber += 1
    if event.getKeys('left') and currentInstructionNumber == 8:
        currentInstructionNumber += 1
    if event.getKeys('right') and currentInstructionNumber == 9:
        currentInstructionNumber += 1
    if event.getKeys('down') and currentInstructionNumber == 10:
        currentInstructionNumber += 1
    if event.getKeys('up') and currentInstructionNumber == 11:
        currentInstructionNumber += 1
    
    if currentInstructionNumber == 13:
        continueRoutine = False
    
    currentInstructionString = str(currentInstructionNumber)
    if currentInstructionNumber < 10:
        currentInstructionString = "0" + currentInstructionString
    currentInstructionFile = instructionSlides + "Slide" + currentInstructionString + ".jpg"
    
    
    # *user_start_signal* updates
    if t >= 0 and user_start_signal.status == NOT_STARTED:
        # keep track of start time/frame for later
        user_start_signal.tStart = t
        user_start_signal.frameNStart = frameN  # exact frame index
        user_start_signal.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(user_start_signal.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if user_start_signal.status == STARTED:
        theseKeys = event.getKeys(keyList=['space', 'right', 'left', 'up', 'down'])
        if len(theseKeys) > 0:  # at least one key was pressed
            user_start_signal.keys = theseKeys[-1]  # just the last key pressed
            user_start_signal.rt = user_start_signal.clock.getTime()
    
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
    for thisComponent in instructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "instructions"-------
for thisComponent in instructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if user_start_signal.keys in ['', [], None]:  # No response was made
    user_start_signal.keys=None
thisExp.addData('user_start_signal.keys',user_start_signal.keys)
if user_start_signal.keys != None:  # we had a response
    thisExp.addData('user_start_signal.rt', user_start_signal.rt)
thisExp.nextEntry()
# the Routine "instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "Practicehand"-------
t = 0
PracticehandClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
if trialDebugMode:
    continueRoutine = False
key_resp_15 = event.BuilderKeyResponse()
# keep track of which components have finished
PracticehandComponents = [theHand, key_resp_15]
for thisComponent in PracticehandComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "Practicehand"-------
while continueRoutine:
    # get current time
    t = PracticehandClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # moving hand when arrow keys are clicked during the main part of the trial
    if event.getKeys([right_key]):
        if handPosition[0] < .8:
            handPosition = (handPosition[0] + .1, handPosition[1])
    if event.getKeys([left_key]):
        if handPosition[0] > -.8:
            handPosition = (handPosition[0] - .1, handPosition[1])
    if event.getKeys([up_key]):
        if handPosition[1] < .8:
            handPosition = (handPosition[0], handPosition[1] + .1)
    if event.getKeys([down_key]):
        if handPosition[1] > -.8:
            handPosition = (handPosition[0], handPosition[1] - .1)
    
    # *theHand* updates
    if t >= 0 and theHand.status == NOT_STARTED:
        # keep track of start time/frame for later
        theHand.tStart = t
        theHand.frameNStart = frameN  # exact frame index
        theHand.setAutoDraw(True)
    frameRemains = 0 + 20- win.monitorFramePeriod * 0.75  # most of one frame period left
    if theHand.status == STARTED and t >= frameRemains:
        theHand.setAutoDraw(False)
    if theHand.status == STARTED:  # only update if drawing
        theHand.setPos(handPosition, log=False)
    
    # *key_resp_15* updates
    if t >= 0.0 and key_resp_15.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_15.tStart = t
        key_resp_15.frameNStart = frameN  # exact frame index
        key_resp_15.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_15.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_15.status == STARTED:
        theseKeys = event.getKeys(keyList=['space'])
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_15.keys = theseKeys[-1]  # just the last key pressed
            key_resp_15.rt = key_resp_15.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in PracticehandComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Practicehand"-------
for thisComponent in PracticehandComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# check responses
if key_resp_15.keys in ['', [], None]:  # No response was made
    key_resp_15.keys=None
thisExp.addData('key_resp_15.keys',key_resp_15.keys)
if key_resp_15.keys != None:  # we had a response
    thisExp.addData('key_resp_15.rt', key_resp_15.rt)
thisExp.nextEntry()
# the Routine "Practicehand" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "get_ready"-------
t = 0
get_readyClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_16 = event.BuilderKeyResponse()
currentInstructionNumber = 15

if trialDebugMode:
    continueRoutine = False
# keep track of which components have finished
get_readyComponents = [InstructSlide14, key_resp_16]
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
    
    # *key_resp_16* updates
    if t >= 0.0 and key_resp_16.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_16.tStart = t
        key_resp_16.frameNStart = frameN  # exact frame index
        key_resp_16.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(key_resp_16.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if key_resp_16.status == STARTED:
        theseKeys = event.getKeys(keyList=['right'])
        if len(theseKeys) > 0:  # at least one key was pressed
            key_resp_16.keys = theseKeys[-1]  # just the last key pressed
            key_resp_16.rt = key_resp_16.clock.getTime()
            # a response ends the routine
            continueRoutine = False
    # all slides advance with a space, except for the last one
    if event.getKeys('space') and currentInstructionNumber != 19:
        currentInstructionNumber += 1
    elif event.getKeys('right') and currentInstructionNumber == 19:
        currentInstructionNumber += 1
    
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
# check responses
if key_resp_16.keys in ['', [], None]:  # No response was made
    key_resp_16.keys=None
thisExp.addData('key_resp_16.keys',key_resp_16.keys)
if key_resp_16.keys != None:  # we had a response
    thisExp.addData('key_resp_16.rt', key_resp_16.rt)
thisExp.nextEntry()

# the Routine "get_ready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# set up handler to look after randomisation of conditions etc
Trial_loop = data.TrialHandler(nReps=30, method='sequential', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Trial_loop')
thisExp.addLoop(Trial_loop)  # add the loop to the experiment
thisTrial_loop = Trial_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial_loop.rgb)
if thisTrial_loop != None:
    for paramName in thisTrial_loop.keys():
        exec(paramName + '= thisTrial_loop.' + paramName)

for thisTrial_loop in Trial_loop:
    currentLoop = Trial_loop
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_loop.rgb)
    if thisTrial_loop != None:
        for paramName in thisTrial_loop.keys():
            exec(paramName + '= thisTrial_loop.' + paramName)
    
    # ------Prepare to start Routine "Eggs"-------
    t = 0
    EggsClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    # indicator variable to track if it's time to pop the balloon
    timeToCrack = 0
    startedTrial = 0
    
    currentEggSettings = eggSettings.pop(0)
    eggPosition = (currentEggSettings[0], .85)
    eggShift = (currentEggSettings[1], currentEggSettings[2])
    handPosition = (-.7, .6)
    eggDegrees = 0
    
    # log info
    currentTrial += 1
    totalKeyPresses = 0
    totalValidKeyPresses = 0
    justCrackedEgg = 0
    updateLog = 0
    
    if trialDebugMode:
        if currentTrial != debugTrial:
            print "This trial is " + str(currentTrial) + ", debug trial is " + str(debugTrial)
            continue
    antic_background.setImage(media + "T2_Anticipatory_background.jpg")
    # keep track of which components have finished
    EggsComponents = [antic_background, avoid_background, egg, the_hand, aversive_crack, ITI]
    for thisComponent in EggsComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Eggs"-------
    while continueRoutine:
        # get current time
        t = EggsClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # initializing defaults for logs
        keyJustPressed = '0'
        validKeyPress = 'NA'
        
        
        # moving hand when arrow keys are clicked during the main part of the trial
        if startedTrial and not timeToCrack:
            if event.getKeys([right_key]):
                updateLog = 1
                keyJustPressed = 'right'
                totalKeyPresses += 1
                validKeyPress = '0'
                if handPosition[0] < .8:
                    handPosition = (handPosition[0] + .1, handPosition[1])
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([left_key]):
                updateLog = 1
                keyJustPressed = 'left'
                totalKeyPresses += 1
                validKeyPress = '0'
                if handPosition[0] > -.8:
                    handPosition = (handPosition[0] - .1, handPosition[1])
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([up_key]):
                updateLog = 1
                keyJustPressed = 'up'
                totalKeyPresses += 1
                validKeyPress = '0'
                if handPosition[1] < .8:
                    handPosition = (handPosition[0], handPosition[1] + .1)
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            elif event.getKeys([down_key]):
                updateLog = 1
                keyJustPressed = 'down'
                totalKeyPresses += 1
                validKeyPress = '0'
                if handPosition[1] > -.8:
                    handPosition = (handPosition[0], handPosition[1] - .1)
                    validKeyPress = '1'
                    totalValidKeyPresses += 1
            else:
                keyJustPressed = ''.join(event.getKeys())
                if keyJustPressed != '':
                    updateLog = 1
                    totalKeyPresses += 1
                    validKeyPress = '0'
        
        # moving the egg during the main part of the trial
        if not timeToCrack and startedTrial:
            eggPosition = (egg.pos[0] + eggShift[0], egg.pos[1] + eggShift[1])
            eggDegrees += 5
        
        # signaling when the main part of the trial has started
        if t > anticipatoryPeriod:
            startedTrial = 1
        
        # if balloon reaches top, balloon will pop (so don't need the success component)
        if egg.pos[1] < -.85:
            if timeToCrack == 0:
                justCrackedEgg= 1
                updateLog = 1
            else:
                justCrackedEgg = 0
            timeToCrack = 1
        
        
        # logging
        logInfo = [id, str(datetime.now()), str(currentTrial), str(t), str(egg.pos[0]), str(egg.pos[1]), 
            str(the_hand.pos[0]), str(the_hand.pos[1]), keyJustPressed, validKeyPress, str(totalKeyPresses), str(totalValidKeyPresses), 
            str(justCrackedEgg)]
        
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
        if (t > anticipatoryPeriod) and avoid_background.status == NOT_STARTED:
            # keep track of start time/frame for later
            avoid_background.tStart = t
            avoid_background.frameNStart = frameN  # exact frame index
            avoid_background.setAutoDraw(True)
        if avoid_background.status == STARTED and bool(timeToCrack):
            avoid_background.setAutoDraw(False)
        
        # *egg* updates
        if t >= 4.0 and egg.status == NOT_STARTED:
            # keep track of start time/frame for later
            egg.tStart = t
            egg.frameNStart = frameN  # exact frame index
            egg.setAutoDraw(True)
        if egg.status == STARTED and bool(timeToCrack):
            egg.setAutoDraw(False)
        if egg.status == STARTED:  # only update if drawing
            egg.setPos(eggPosition, log=False)
            egg.setOri(eggDegrees, log=False)
            egg.setSize((0.1, 0.1), log=False)
        
        # *the_hand* updates
        if t >= 4 and the_hand.status == NOT_STARTED:
            # keep track of start time/frame for later
            the_hand.tStart = t
            the_hand.frameNStart = frameN  # exact frame index
            the_hand.setAutoDraw(True)
        if the_hand.status == STARTED and bool(timeToCrack):
            the_hand.setAutoDraw(False)
        if the_hand.status == STARTED:  # only update if drawing
            the_hand.setPos(handPosition, log=False)
        # start/stop aversive_crack
        if (timeToCrack) and aversive_crack.status == NOT_STARTED:
            # keep track of start time/frame for later
            aversive_crack.tStart = t
            aversive_crack.frameNStart = frameN  # exact frame index
            aversive_crack.play()  # start the sound (it finishes automatically)
        
        # *ITI* updates
        if (timeToCrack) and ITI.status == NOT_STARTED:
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
        for thisComponent in EggsComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Eggs"-------
    for thisComponent in EggsComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # need to get egg offscreen in the positive direction
    egg.pos[1] = 2
    aversive_crack.stop()  # ensure sound has stopped at end of routine
    # the Routine "Eggs" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 30 repeats of 'Trial_loop'


# ------Prepare to start Routine "thanks"-------
t = 0
thanksClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_14 = event.BuilderKeyResponse()
# keep track of which components have finished
thanksComponents = [Thankyou, key_resp_14]
for thisComponent in thanksComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "thanks"-------
while continueRoutine:
    # get current time
    t = thanksClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *Thankyou* updates
    if t >= 0.0 and Thankyou.status == NOT_STARTED:
        # keep track of start time/frame for later
        Thankyou.tStart = t
        Thankyou.frameNStart = frameN  # exact frame index
        Thankyou.setAutoDraw(True)
    
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
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
