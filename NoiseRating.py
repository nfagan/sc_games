#!/usr/bin/env python2

# psychopy wants this import, and __future__ must be the first line of code when it's used
from __future__ import absolute_import, division

# script-specific imports (more psychopy imports will come later, after parsing input options)
import os, sys, re 
from optparse import OptionParser, SUPPRESS_HELP
from datetime import datetime
from random import shuffle


## Task constants
project_dir = os.path.dirname(os.path.abspath(__file__)) # this script should be located directly in the project directory

# path of folder containing the sounds (if this folder doesn't exist, the script has been moved or the project directory isn't clean)
media = project_dir + '/sc_media/'
if not os.path.isdir(media):
    print "Error: Could not find project media directory %s." % media
    print "Make sure your copy of this script is located in its proper project directory, which should contain all necessary files."

# slides that are cycled through for each sound to be rated
instruction_slide = media + 'Noise_Rating_Slides/InstructionSlide.jpg'
rating_slide = media + 'Noise_Rating_Slides/RatingSlide.jpg'
fixation_slide = media + 'iti_background.jpg'

# The sounds to be played, the order of which is randomized for each run
sounds_to_rate = [media + 'chime.wav', media + 'Balloon_Pop.wav', media + 'SHAPES_USE.wav', media + 'egg_crack.wav']
shuffle(sounds_to_rate)

# window size
screen_width = 1440
screen_height = 900

## Define, collect, and validate runtime options
parser = OptionParser()
parser.add_option("-i", "--participant-id", metavar="ID", dest="participant_id", help="the participant ID")
parser.add_option("-o", "--output", metavar="OUTPUT_DIR", dest="output_dir", help="the directory where output/logs should be saved")
parser.add_option("-v", "--version", metavar="VERSION", dest="version", help=SUPPRESS_HELP, default="unknown")

(options, args) = parser.parse_args()
output_dir = options.output_dir
participant_id = options.participant_id
version = options.version

if not project_dir or not output_dir or not participant_id:
    parser.print_help()
    sys.exit()

game_type = "noise_rating"
output_dir = re.sub('\/+$', '', output_dir) # strip trailing slashes
timestamp = datetime.strftime(datetime.now(),  "%b-%d-%y_%H%M")
if not os.path.isdir(output_dir):
    print "Error: Output destination %s does not exist." % output_dir
    sys.exit()
else:
    output_dir = os.path.abspath(output_dir)
    output_dir += "/%s/%s_%s" % (participant_id, game_type, timestamp)
    if os.path.exists(output_dir):
        print "Error: Run-specific output directory %s already exists." % output_dir
        sys.exit()
    else:
        try:
            os.makedirs(output_dir)
        except:
            print "Error: Could not create output directory %s." % output_dir
            print "Are you sure that directory is writeable?"
            sys.exit()


# more psychopy imports
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

# Setup the task window
win = visual.Window(size=(screen_width, screen_height), fullscr=True,allowGUI=False, monitor='testMonitor', blendMode='avg', useFBO=True)

# store frame rate of monitor if we can measure it
exp_info = {}
exp_info['frame_rate'] = win.getActualFrameRate()
exp_info['participant_id'] = participant_id

# Store info about the experiment session
exp_name = game_type
exp_info['date'] = timestamp
exp_info['exp_name'] = exp_name

# Doing some logging with Psychopy's ExperimentHandler class
exp_handler_log = "%s/psychopy" % output_dir
this_exp = data.ExperimentHandler(name=exp_name, version='',
    extraInfo=exp_info, runtimeInfo=None,
    savePickle=True, saveWideText=False,
    dataFileName=exp_handler_log)
# save a log file for detail verbose info
logFile = logging.LogFile(exp_handler_log +'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# Check that participant ID is valid
valid_id_pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
if not re.search(valid_id_pattern, participant_id):
    print "Error: Invalid or missing participant ID."
    print "The participant ID must start with a letter or number, and it can only contain numbers, letters, hyphens, and underscores."
    core.quit()

# Open the output file and write headers
output_file = "%s/ratings_%s_%s.txt" % (output_dir, participant_id, timestamp)
f = open(output_file, 'w')
f.write("# Version: %s\n" % version)
f.write("Participant\tSound\tRating\n")


# define the components for the task: a screen-sized image for instructions/ratings, and a sound to play
slide = visual.ImageStim(win=win, name='Slide', image='sin', size=(screen_width, screen_height), interpolate=True)
slide.autoDraw = True
sound_component = sound.Sound('A', secs=-1) # "A" is a placeholder sound
rating_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9'] # sounds get rated 1-9

# run the task
for current_sound in sounds_to_rate:
    sound_component.setSound(current_sound)
    slide.setImage(instruction_slide)
    win.flip() # causes instruction slide to be drawn now
    event.waitKeys(keyList = ['space']) # wait for user to request sound
    slide.setImage(fixation_slide)
    win.flip()
    core.wait(0.5)
    sound_component.play()
    while sound_component.status != FINISHED:
        pass
    slide.setImage(rating_slide)
    win.flip()
    while True:
        key_list = event.waitKeys(keyList = rating_keys)
        # have to account for the rare situation where two keys are pressed at once (ignoring input in that case)
        if len(key_list) == 1:
            break
    current_rating = key_list[0]
    f.write("%s\t%s\t%s\n" % (participant_id, current_sound, current_rating))

# clean up
slide.autoDraw = False
win.flip()
f.close()
print "Finished run!"
print "Output has been written to %s." % output_dir

# Psychopy's shutdown code
this_exp.saveAsPickle(exp_handler_log)
logging.flush()
this_exp.abort()
win.close()
core.quit()
