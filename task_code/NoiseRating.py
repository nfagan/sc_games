#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.2),
    on Sat Apr  8 22:39:17 2017
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
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
expName = 'noise'  # from the Builder filename that created this script
expInfo = {u'participantID': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = '/Users/ecohodes/Dropbox/sc/sc_output/NoiseRating/logs/%s_%s' % (expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/ecohodes/Dropbox/sc/Noise Rating/NoiseRating.psyexp',
    savePickle=True, saveWideText=True,
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
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
# Project directory (change this and the log directory declared
# "Experiment Settings" if moving to a new environment)
projectDir = '/Users/ecohodes/Dropbox/sc/'

# path of folder containing the sounds
media = projectDir + 'sc_media/'
outputDir = projectDir + 'sc_output/NoiseRating/'

# A and B are Psychopy placeholders for the netural sounds
soundsToRate = [media + 'chime.wav', media + 'Balloon_Pop.wav', media + 'SHAPES_USE.wav', media + 'egg_crack.wav']

# slides that are cycled through for each sound to be rated
instructionSlide = media + 'Noise_Rating_Slides/InstructionSlide.jpg'
ratingSlide = media + 'Noise_Rating_Slides/RatingSlide.jpg'
fixationSlide = media + 'iti_background.jpg'

# start off with the instruction slide and the first sound
currentSlide = instructionSlide
playSoundNow = False

# valid participant ID
import re
pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
if not re.search(pattern, expInfo['participantID']):
    print "Error: Invalid or missing participant ID."
    print "The participant ID must start with a letter or number, and it can only contain numbers, letters, hyphens, and underscores."
    core.quit()

outputFile = outputDir + "noise_ratings_%s.txt" % expInfo['participantID']
f = open(outputFile, 'w')
f.write("Participant\tNoise\tRating\n")
Slide = visual.ImageStim(
    win=win, name='Slide',
    image='sin', mask=None,
    ori=0, pos=(0, 0), size=(2, 2),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
soundToRate = sound.Sound('A', secs=-1)
soundToRate.setVolume(1)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
sounds = data.TrialHandler(nReps=4, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='sounds')
thisExp.addLoop(sounds)  # add the loop to the experiment
thisSound = sounds.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisSound.rgb)
if thisSound != None:
    for paramName in thisSound.keys():
        exec(paramName + '= thisSound.' + paramName)

for thisSound in sounds:
    currentLoop = sounds
    # abbreviate parameter names if possible (e.g. rgb = thisSound.rgb)
    if thisSound != None:
        for paramName in thisSound.keys():
            exec(paramName + '= thisSound.' + paramName)
    
    # ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    currentSound = soundsToRate.pop(0)
    key_listener = event.BuilderKeyResponse()
    soundToRate.setSound(currentSound, secs=1)
    # keep track of which components have finished
    trialComponents = [key_listener, Slide, soundToRate]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if currentSlide == instructionSlide and event.getKeys('space'):
            currentSlide = fixationSlide
           
        
        elif currentSlide == fixationSlide:
            # if the sound hasn't been played, wait a short period and then play it
            if soundToRate.status != FINISHED:
                core.wait(0.5)
                playSoundNow = True
            # if the sound is finished playing, go to the next slide
            else:
                currentSlide = ratingSlide
                playSoundNow = False
        
        elif currentSlide == ratingSlide:
            keys = event.getKeys()
            try:
                rating = int(keys[0])
            except:
                pass
            else:
                f.write("%s\t%s\t%d\n" %(expInfo['participantID'], currentSound, rating))
                currentSlide = instructionSlide
                continueRoutine = False
        
        
        
        
        
        
        
        
        
        # *key_listener* updates
        if t >= 0.0 and key_listener.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_listener.tStart = t
            key_listener.frameNStart = frameN  # exact frame index
            key_listener.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_listener.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_listener.status == STARTED:
            theseKeys = event.getKeys()
            if len(theseKeys) > 0:  # at least one key was pressed
                key_listener.keys = theseKeys[-1]  # just the last key pressed
                key_listener.rt = key_listener.clock.getTime()
        
        # *Slide* updates
        if t >= 0 and Slide.status == NOT_STARTED:
            # keep track of start time/frame for later
            Slide.tStart = t
            Slide.frameNStart = frameN  # exact frame index
            Slide.setAutoDraw(True)
        if Slide.status == STARTED:  # only update if drawing
            Slide.setImage(currentSlide, log=False)
        # start/stop soundToRate
        if (playSoundNow) and soundToRate.status == NOT_STARTED:
            # keep track of start time/frame for later
            soundToRate.tStart = t
            soundToRate.frameNStart = frameN  # exact frame index
            soundToRate.play()  # start the sound (it finishes automatically)
        if soundToRate.status == STARTED and t >= (soundToRate.tStart + 1):
            soundToRate.stop()  # stop the sound (if longer than duration)
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # check responses
    if key_listener.keys in ['', [], None]:  # No response was made
        key_listener.keys=None
    sounds.addData('key_listener.keys',key_listener.keys)
    if key_listener.keys != None:  # we had a response
        sounds.addData('key_listener.rt', key_listener.rt)
    soundToRate.stop()  # ensure sound has stopped at end of routine
    # the Routine "trial" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 4 repeats of 'sounds'

print "Finished run!"

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
