#!/usr/bin/env python2

"""
This script runs three conditions Magic Balloon Game: Controllable stress, uncontrollable stress, and non-stressed.
Soon, it will also run the Magic Egg Game.
"""

# Psychopy wants this
from __future__ import absolute_import, division

# Psychopy has lots of additional imports, but they'll get imported after runtime options are validated to prevent task window from launching before it's necessary
import os, sys
import re, pickle
from optparse import OptionParser, SUPPRESS_HELP
from datetime import datetime
from subprocess import call
from random import shuffle, choice

# Labjack-related imports
import u3
from time import sleep
from threading import Thread

# The project source directory is taken to be the directory containing this script
project_dir = os.path.dirname(os.path.abspath(__file__))

# Media subdirectory should be present in project folder    
media = project_dir + "/media/"
if not os.path.isdir(media):
    print "Error: Could not find required directory %s in the project source folder." % media
    print "Make sure you have a clean copy of this project's source repository."
    sys.exit()

# Egg media files
whole_egg_image = media + "egg.png"
cracking_egg_1_image = media + "cracking_egg_1.png"
cracking_egg_2_image = media + "cracking_egg_2.png"
egg_anticipatory_background = media + "Egg_anticipatory_background.jpg"
egg_avoidance_background =  media + "Egg_avoidance_background.jpg"
cracking_sound = media + "Sounds/egg_crack.wav"
egg_slide_dir = media + "Egg_instruction_slides/"

# Balloon media files
whole_balloon_image = media + "pink_balloon.png"
pop_1_image = media + "pop_1.png"
pop_2_image = media + "pop_2.png"
balloon_anticipatory_background = media + "Balloon_anticipatory_background.jpg"
balloon_avoidance_background = media + "Balloon_avoidance_background.jpg"
popping_sound = media + "Sounds/balloon_pop.wav"
balloon_slide_dir = media + "Balloon_instruction_slides/"

# Collision files show which x/y distances between objects should count as collisions
balloon_wand_collision_file = project_dir + "/resources/balloon_wand_collision_map.pickle"
egg_wand_collision_file = project_dir + "/resources/egg_wand_collision_map.pickle"
balloon_hand_collision_file = project_dir + "/resources/balloon_hand_collision_map.pickle"
egg_hand_collision_file = project_dir + "/resources/egg_hand_collision_map.pickle"


# Experiment parameters
balloon_modes = (cs, us, ns) = ("balloon_cs", "balloon_us", "balloon_ns")
all_modes = balloon_modes + ("egg",)
screen_width = 1440
screen_height = 900
num_trials = 30
down_key = "down" # Note that these all get redefined when running in button box mode
left_key = "left"
up_key = "up"
right_key = "right"
expected_fps = 60
win_refresh_threshold = 1.0/expected_fps + 0.004 # defining what counts as a dropped frame (value suggested by Psychopy site)

# Labjack event mappings (correspond to FIO port numbers)
lj_events = { "avoidance_onset":4, "first_contact":5, "aversive_sound":6, "no_aversive_sound":7 }

# Constants used across balloon/egg games
implement_practice_time = 20.0
antic_period_duration = 4
avoidance_period_duration = 4.5
ITI_duration = 10 # need a long inter-trial period for MRI synching
implement_step_size = 80 # distance wand or hand moves per step (in pixels)
magic_sparks_duration = 0.75 # duration of magic sparks effect upon touching target object

# Balloon game constants
balloon_Y_start = int(-screen_height/2)
balloon_Y_speed = 6
sparks_balloon_offset_x = 5
sparks_balloon_offset_y = 30
balloon_catch_y_boundary = .85 * screen_height/2
balloon_catch_boundary_direction = '>'
balloon_implement_start_position = (0, -360)
balloon_rotation_rate = 0 # degrees/frame

# Define per-trial balloon starting X/Y positions, X/Y per-frame step (speed), and a list of vertical "zig"  lines
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

# Egg game constants
egg_Y_start = int(.85 * screen_height/2)
egg_zigs = [] # no zigging in egg game
egg_implement_start_position = (-504, 270)
egg_rotation_rate = 5 # degrees/frame

# Define per-trial balloon starting X/Y positions, X/Y per-frame step (speed), and zig lines
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
egg_catch_y_boundary = -.85 * screen_height/2
egg_catch_boundary_direction = '<'


# standard runtime options
parser = OptionParser()
parser.add_option("-i", "--participant-id", metavar="ID", dest="participant_id", help="the participant ID")
parser.add_option("-o", "--output", metavar="OUTPUT_DIR", dest="output_dir", help="the directory where output data and log files should be saved")
parser.add_option("-g", "--game-type", metavar="GAME", dest="game_type", choices=("magic", "mundane"),
    help="the type of exeriment to run: \"magic\" (with wand) or \"mundane\" (with hand)")
parser.add_option("-m", "--game-mode", metavar="MODE", dest="mode", choices=all_modes, help="the game mode (choices: %s)" % str(all_modes))
parser.add_option("-y", "--yoke-source", metavar="YOKE_FILE", dest="yoke_source", help="For balloon_us and balloon_ns conditions, indicate a yoking file from a balloon_cs run")
parser.add_option("-B", "--button-box", action="store_true", default=False, dest="button_box_mode", help="use button box input (1-4 instead of right, down, left, up)")

# options for testing and development
parser.add_option("--fast", action="store_true", default=False, dest="fast_mode", help="use shortened ITI and anticipatory periods (for test runs only)")
parser.add_option("--skip-instructions", action="store_true", default=False, dest="skip_instructions", help="skip instructions/practice slides (for test runs only)")
parser.add_option("--debug-trial", metavar="TRIAL_NUMBER", dest="debug_trial", help="test a specific trial and skip everything else")

# to specify git version of project (wrapper script supplies automatically if it finds a clean repository; don't fake it by supplying your own value!)
parser.add_option("-v", "--version", metavar="VERSION", dest="version", help=SUPPRESS_HELP, default="unknown")

# collect runtime options
(options, args) = parser.parse_args()
output_dir = options.output_dir
participant_id = options.participant_id
game_type = options.game_type
mode = options.mode
yoke_source = options.yoke_source

version = options.version
button_box_mode = options.button_box_mode
fast_mode = options.fast_mode
skip_instructions = options.skip_instructions
trial_debug_requested = options.debug_trial

# validate runtime options
if not output_dir or not participant_id or not game_type or not mode:
    parser.print_help()
    sys.exit()

valid_id_pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
if not re.search(valid_id_pattern, participant_id):
    print "Error: Illegal participant ID."
    print "ID must start with a letter or number, and may only contain letters, numbers, hyphens, and underscores."
    sys.exit()

output_dir = re.sub('\/+$', '', output_dir) # strip trailing slashes
timestamp = datetime.strftime(datetime.now(),  "%b-%d-%y_%H%M")
if not os.path.isdir(output_dir):
    print "Error: Output destination %s does not exist." % output_dir
    sys.exit()
else:
    output_dir = os.path.abspath(output_dir)
    output_dir += "/%s/%s_%s_%s" % (participant_id, game_type, mode, timestamp)
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

# Declare additional variables based on the runtime options
full_data_file = "%s/%s_%s_%s_%s_full.txt" % (output_dir, participant_id, game_type, mode, timestamp)
highlight_data_file = "%s/%s_%s_%s_%s_highlights.txt" % (output_dir, participant_id, game_type, mode, timestamp)

# determine game type (magic or non-magic)
playing_magic_game = True if game_type == "magic" else False
playing_hand_game = not playing_magic_game

# determine which game mode we're playing: balloon game comes in cs/us/ns, egg game always uncontrollable stress (us)
playing_balloon_game = True if mode in balloon_modes else False
playing_egg_game = not playing_balloon_game
nonstressed_mode = True if mode == ns else False

# handle yoking of aversive sound outcomes for the uncontrollable stress condition
if not mode == us and yoke_source:
    print "Error: A yoking source file has been specified even though the game type requested does not involve yoking."
    sys.exit()
if mode == us:
    if not yoke_source:
        print "Error: The requested game type requires a yoking source file (re-run with \"--help\" for more information.)"
        sys.exit()
    if not re.search('\.pickle$', yoke_source):
        print "Error: The yoking file specified does not seem proper, as its name does not end in \".pickle\"."
        sys.exit()
    if not os.path.isfile(yoke_source):
        print "Error: The specified yoking file could not be found."
        sys.exit()
    yoke_source = os.path.abspath(yoke_source)
    # read in the pickle from the source
    with open(yoke_source, 'r') as y:
        aversive_sound_by_trial_num = pickle.load(y)
    # make sure the source participant had the same number of trials as the current run
    num_trials_in_yoke_source = len(aversive_sound_by_trial_num)
    if num_trials_in_yoke_source != num_trials:
        print "Error: The yoking source file contained data for %d trials, not the expected %d trials." % (num_trials_in_yoke_source, num_trials)
        sys.exit()
else:
    aversive_sound_by_trial_num = {} # Keys = trial number, values = True/False on whether aversive sound should play

if button_box_mode:
    down_key = "1" # green
    left_key = "2" # red
    up_key = "3" # blue
    right_key = "4" # yellow

if trial_debug_requested:
    trial_debug_mode = True
    debug_trial = int(trial_debug_requested)
    skip_instructions = True
    fast_mode = True
else:
    trial_debug_mode = False

if fast_mode: 
    ITI_duration = 1
    antic_period_duration = 1

# will pull from balloon/egg settings list in random order (unless testing trials)
all_trajectory_info = egg_trajectory_info if playing_egg_game else balloon_trajectory_info
trajectory_order = range(0, len(all_trajectory_info))
if not trial_debug_mode and not fast_mode and not skip_instructions: 
    shuffle(trajectory_order)

## Set task-specific constants depending on whether egg or balloon game is being played
# read in target-implement collision file (created by CollisionMapMaker)
if playing_magic_game:
    collision_file = egg_wand_collision_file if playing_egg_game else balloon_wand_collision_file
else:
    collision_file = egg_hand_collision_file if playing_egg_game else balloon_hand_collision_file

with open(collision_file) as cf:
   collision_space_by_y = pickle.load(cf)

catchable_area_y_boundary = egg_catch_y_boundary if playing_egg_game else balloon_catch_y_boundary
boundary_direction = egg_catch_boundary_direction if playing_egg_game else balloon_catch_boundary_direction
instruction_slide_dir = egg_slide_dir if playing_egg_game else balloon_slide_dir


## Try to interface with Labjack
labjack_active = False # gets set to true upon successful initiation of U3 object
try:
    device = u3.U3()
    labjack_active = True
except:
    get_confirm = raw_input("Warning: Unable to interface with Labjack. GSR triggers won't be sent. Would you like to continue (y/n)? ")
    while True:
        if get_confirm == "y" or get_confirm == "yes":
            break
        elif get_confirm == "n" or get_confirm == "no":
            try:
                os.rmdir(output_dir)
            except:
                pass
            print "Aborted experiment."
            sys.exit()
        get_confirm = raw_input("Invalid response. Enter \"y\" to continue, \"n\" to quit: ")

if labjack_active:
    lj_log = output_dir + "/labjack.log"
    global lj
    lj = open (lj_log, 'w')
    lj.write("#" + str(device.getCalibrationData()) + "\n")
    lj.write("time\tport\tdescription\n")

def send_labjack_event(event_type):
    if not labjack_active:
        return
    if event_type not in lj_events:
        print "Warning: invalid event type (%s) could not be handled as a GSR trigger." % event_type
        return
    fio_num = lj_events[event_type]
    timestamp = str(datetime.now())
    lj.write("%s\t%d\t%s\n" % (timestamp, fio_num, event_type))
    lj.flush()
    trigger_thread = Thread(target=labjack_event_handler, args=(fio_num,))
    trigger_thread.start()

def labjack_event_handler(fio_num):
    device.setFIOState(fio_num, state=1)
    sleep(1)
    device.setFIOState(fio_num, state = 0)


## Now going to start loading Psychopy and setting up the experiment window
# Psychopy uses all this stuff, supposedly
from psychopy import data
from psychopy import locale_setup, sound, gui, visual, core, event, logging
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from numpy import (sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray)

# Set up logging using ExperimentHandler
exp_info = {} # a dict of run information that gets passed to the ExperimentHandler
exp_info['date'] = timestamp 
exp_info['exp_name'] = mode
exp_handler_log = "%s/psychopy" % output_dir
this_exp = data.ExperimentHandler(name=mode, extraInfo=exp_info, savePickle=True, saveWideText=False, dataFileName=exp_handler_log)
log_file = logging.LogFile(exp_handler_log+'.log', level=logging.EXP)
#logging.console.setLevel(logging.WARNING) # makes warnings get printed to console window

# Set up the experiment window (there are additional options you can specify; see documentation if you ever care)
win = visual.Window(size=(screen_width, screen_height), fullscr=True, allowGUI=False, useFBO=True, units='pix', monitor = 'testMonitor')
calculated_fps = int(round(win.getActualFrameRate()))
if calculated_fps != expected_fps:
    print "Warning: This experiment is meant to run at %d frames per second, but your display was recorded at %d fps." % (expected_fps, calculated_fps)
    print "(If you're within a couple of frames, there's no need to worry about this.)"

# Having dropped frames recorded (will access later with win.nDroppedFrames)
win.recordFrameIntervals = True
win.refreshThreshold = win_refresh_threshold


## Declare all the ImageStim, TextStim, and Sound objects that are used through the experiment
# The image component used for instruction slide routines (instructions_1, instructions_2, and the thank you message at the end)
slides = visual.ImageStim(win = win, name = 'slides', units='pix', image='sin', size=(screen_width, screen_height), interpolate=True, depth=-2.0)

# Components for implement (hand/wand) practice routine
if playing_magic_game:
    implement = visual.ImageStim(win=win, name='wand',units='pix', image=media + "magic_wand.png", pos=[0,0], interpolate=True, depth=-4.0)
else:
    implement = visual.ImageStim(win=win, name='hand',units='pix', image=media + "orange_hand.png", pos=[0,0], interpolate=True, depth=-4.0)
time_left_label = visual.TextStim(win=win, name='time_left_label', text=None, font='Arial', units='norm', pos=(.9, -.8), height=0.1, wrapWidth=None, color='#053270', depth=-2.0);

# Components for all routines (except wand or hand, which was declared above)
ITI = visual.ImageStim(win=win, name='ITI',units='pix', image=media + "iti_background.jpg", 
    pos=(0, 0), size=(screen_width, screen_height), interpolate=True, depth=-6.0)
counter_background = visual.ImageStim(win=win, name='counter_background',units='pix', 
    image=media + "label_background.png", pos=(550, -435), size=(175, 45), interpolate=True, depth=-7.0, opacity=0)
counter = visual.TextStim(win=win, name='counter', text=None, font=u'Arial', units='pix', pos=(550, -432), height=24,
    wrapWidth=None, color=u'#053270', depth=-8.0, opacity=0);

if playing_magic_game:
    magic_sparks = visual.ImageStim(win=win, name='magic_sparks',units='pix', 
        image=media + "magic_effect.png", pos=[0,0], size=(150, 150), opacity=.75, interpolate=True, depth=-9.0)
    magic_sound = sound.Sound(media + "Sounds/magic_sound.wav", secs=-1, volume = .5)


# Specific components for egg and balloon games
if playing_egg_game:
    target = visual.ImageStim(win = win, name = 'egg', units = 'pix', image = whole_egg_image, interpolate = True, depth = -3.0)
    aversive_sound = sound.Sound(cracking_sound, secs=-1, volume = 1.0)
    antic_background = visual.ImageStim(win=win, name='antic_background',units='pix', image=egg_anticipatory_background, 
        size=(screen_width, screen_height), interpolate=True, depth=-1.0)
    avoid_background = visual.ImageStim(win=win, name='avoid_background',units='pix', image=egg_avoidance_background,
        size=(screen_width, screen_height), interpolate=True, depth=-2.0)
    whole_target_image = whole_egg_image
    implement_starting_position = egg_implement_start_position
    first_break_image = cracking_egg_1_image
    second_break_image = cracking_egg_2_image
    target_rotation_rate = egg_rotation_rate

else:
    target = visual.ImageStim(win=win, name='balloon', units = 'pix', image = whole_balloon_image, interpolate=True, depth = -3.0)
    aversive_sound = sound.Sound(popping_sound, secs=-1, volume = 1.0)
    antic_background = visual.ImageStim(win=win, name='antic_background',units='pix', image=balloon_anticipatory_background, 
        size=(screen_width, screen_height), interpolate=True, depth=-1.0)
    avoid_background = visual.ImageStim(win=win, name='avoid_background',units='pix', image=balloon_avoidance_background,
        size=(screen_width, screen_height), interpolate=True, depth=-2.0)
    whole_target_image = whole_balloon_image
    implement_starting_position = balloon_implement_start_position
    target_rotation_rate = balloon_rotation_rate
    first_break_image = pop_1_image
    second_break_image = pop_2_image

# A routine to simplify task flow
class Routine():
    # A routine consists of a set of associated components (ImageStim, TextStim, Sound), a clock, a frame counter, and a marker to
    # show whether the routine is "live" (that is, has components that are currently active in window).
    # In addition, a routine can have have custom functions that run on startup, shutdown, and on a frame-by-frame basis
    def __init__(self, window = None, startup = None, run_frame = None, shutdown = None):
        self.startup_func = startup
        self.run_frame_func = run_frame
        self.shutdown_func = shutdown
        self.components = set()
        self.live = False
        self.clock = core.Clock()
        self.frameN = -1 # frame number will be 0-based, because that's what Psychopy recommends
        if isinstance(window, visual.Window):
            self.win = window
        else:
            raise ValueError("Window supplied to Routine class is not of type visual.Window")

    # When a routine goes live, its clock is set to 0, and then a custom routine-specific startup code runs (if supplied)
    def startup (self, *args):
        self.live = True
        self.clock.reset()
        if self.startup_func:
            self.startup_func(self, *args)

    # Every frame, the frame count is incremented and then custom code runs, if supplied
    def run_frame(self, *args):
        self.frameN += 1
        if self.run_frame_func: self.run_frame_func(self, *args)
        # Flip window if there are components running (if not, mark routine as no longer live)
        if len(self.components) > 0:
            self.win.flip()
        else:
            self.live = False

    # When shutdown is called, custom code runs (if supplied), and then all components are stopped and removed from the routine
    def shutdown(self, *args):
        if self.shutdown_func:
            self.shutdown_func(self, *args)
        self.stop_all_components()

    # Method to start components (set images to display, sounds to display, and record start-up information for logging)
    def start_component(self, component):
        component.frameNStart = self.frameN  # exact frame index
        component.tStart = self.clock.getTime()
        if isinstance(component, (visual.ImageStim, visual.ShapeStim, visual.TextStim)):
            component.setAutoDraw(True)
        elif isinstance (component, sound.Sound):
            component.play()
        self.components.add(component)

    # Method to stop components (stop displaying images, stop playing sounds, and remove component from routine)
    def stop_component(self, component):
        # do nothing if routine doesn't contain component
        if component not in self.components:
            return
        if isinstance(component, (visual.ImageStim, visual.ShapeStim, visual.TextStim)):
            component.setAutoDraw(False)
        elif isinstance (component, sound.Sound):
            component.stop()
        else:
            return # don't know how to handle other objects, so doing nothing
        self.components.remove(component)

    # Method to stop all components at once
    def stop_all_components(self):
        component_list = list(self.components)
        for component in component_list:
            self.stop_component(component)

    # Simple convenience method that runs a routine in the intended way
    @staticmethod
    def run_routine(routine):
        if not isinstance(routine, Routine):
            raise ValueError("Input to method Routine.run_routine was not an instance of class Routine.")
        routine.startup()
        while routine.live:
            routine.run_frame()
        routine.shutdown()


## Declare all the functions that control the behavior of each routine in the experiment
# for each numbered instruction slide, storing which key press is required to advance
keys_to_advance = {} 
for slide_num in range (1, 10):
    keys_to_advance[slide_num] = 'space'
keys_to_advance[10], keys_to_advance[11], keys_to_advance[12], keys_to_advance[13] = left_key, right_key, down_key, up_key
for slide_num in range(14, 19):
    keys_to_advance[slide_num] = 'space'

def run_slides(routine, current_slide, last_slide):
    if hasattr(routine, "current_slide"):
        current_slide = routine.current_slide
    else:
        routine.current_slide = current_slide
        routine.start_component(slides)

    # first slide stays for 2 seconds (although user can still skip forward with space bar if they try)
    ## TO DO: get rid of this, repalce with a label that appears on some slides
    if (routine.clock.getTime() > 2 and current_slide == 1):
        current_slide += 1

    # most slides advance with the press of the space bar
    keys_pressed = event.getKeys()

    # if multiple keys are pressed in one frame, doing nothing
    if len(keys_pressed) > 1:
        return

    # if a key was pressed, check if it's the right one
    try:
        key_pressed = keys_pressed[0]
        if keys_to_advance[current_slide] == key_pressed:
            current_slide += 1
    except IndexError: pass
    if current_slide > last_slide:
        routine.live = False
        return
    current_slide_string = str(current_slide)
    if current_slide < 10:
        current_slide_string = "0" + current_slide_string
    current_slide_file = instruction_slide_dir + "Slide" + current_slide_string + ".jpg"
    slides.setImage(current_slide_file)
    routine.current_slide = current_slide

def implement_practice_startup(routine):
    routine.start_component(implement)
    routine.start_component(time_left_label)
    routine.rounded_seconds_remaining = int(implement_practice_time)
    time_left_label.setText(str(routine.rounded_seconds_remaining))

def implement_practice_run_frame(routine):
    # move implement if appropriate (only allowing one implement movement per frame)
    keys_pressed = event.getKeys()
    if right_key in keys_pressed:
        if implement.pos[0] + implement.size[0]/2 + implement_step_size < screen_width/2:
            implement.pos = (implement.pos[0] + implement_step_size, implement.pos[1])
    elif left_key in keys_pressed:
        if implement.pos[0] - implement.size[0]/2 - implement_step_size > -screen_width/2: 
            implement.pos = (implement.pos[0] - implement_step_size, implement.pos[1])
    elif up_key in keys_pressed:
        if implement.pos[1] + implement.size[1]/2 + implement_step_size < screen_height/2:
            implement.pos = (implement.pos[0], implement.pos[1] + implement_step_size)
    elif down_key in keys_pressed:
        if implement.pos[1] - implement.size[1]/2 - implement_step_size > -screen_height/2:
            implement.pos = (implement.pos[0], implement.pos[1] - implement_step_size)
    elif "escape" in keys_pressed:
        routine.live = False

    seconds_remaining = implement_practice_time - routine.clock.getTime()
    if seconds_remaining < 0:
        routine.live = False
        return
    if seconds_remaining < (routine.rounded_seconds_remaining - 1):
        routine.rounded_seconds_remaining -= 1
        time_left_label.setText(str(int(routine.rounded_seconds_remaining)))

# define global variables needed by the trial routines
spells_cast = 0
current_trial_num = 0
f = open(full_data_file, 'w')
h = open (highlight_data_file, 'w')

def trial_startup(routine):
    global current_trial_num
    current_trial_num += 1
    routine.target_broken = False
    if mode == us:
        routine.target_doomed = aversive_sound_by_trial_num[current_trial_num]
    elif mode == ns:
        routine.target_doomed = False
    else:
        routine.target_doomed = True
    routine.target_has_been_touched = False
    routine.magic_has_happened = False
    routine.started_avoidance_phase = False
    routine.started_anticipatory_phase = False # doesn't stay false for long
    routine.target_has_exited_catchable_area = False
    routine.started_ITI = False
    routine.trial_num = current_trial_num
    implement.pos = implement_starting_position # becomes visible later
    target.setImage(whole_target_image) # becomes visible later

    # Note that the counter is currently not being used (opacity has been set to 0)
    routine.start_component(antic_background)
    routine.start_component(counter_background)
    routine.start_component(counter)
    counter.setText("Spells cast: %d" % spells_cast)

    # get and apply current trajectory info
    current_trajectory_index = trajectory_order[current_trial_num - 1]
    current_trajectory_info = all_trajectory_info[current_trajectory_index]
    target.pos = current_trajectory_info[0], current_trajectory_info[1]
    routine.target_step = (current_trajectory_info[2], current_trajectory_info[3])
    routine.zigs = current_trajectory_info[4]
    routine.trajectory_description = str(current_trajectory_info)
    if trial_debug_mode or skip_instructions or fast_mode:
        print "Using index %d in trajectory list: " % current_trajectory_index + routine.trajectory_description



def trial_run_frame(routine):
    time_in_trial = routine.clock.getTime()
    t = datetime.now()
    timestamp = datetime.strftime(t, "%H:%M:%S.%f")
    time_in_seconds = t.hour * 3600 + t.minute * 60 + t.second + t.microsecond/1000000.0
    X_target, Y_target, X_implement, Y_implement = ['NA'] * 4
    keyboard_used, keys_pressed, implement_move_direction = ['NA'] * 3
    target_zigged, touching_target_object, target_outside_catchable_area = ['NA'] * 3
    just_made_magic, just_made_first_contact, target_just_exited_catchable_area, aversive_noise_onset, antic_period_onset, avoid_period_onset, iti_onset, trial_offset = ['0'] * 8

    def write_to_data_files():
        output_fields = [participant_id, str(routine.trial_num), timestamp, str(time_in_seconds), str(time_in_trial), str(X_target), str(Y_target), 
            str(X_implement), str(Y_implement), keyboard_used, keys_pressed, implement_move_direction, target_zigged, touching_target_object, target_outside_catchable_area, 
            just_made_magic, just_made_first_contact, target_just_exited_catchable_area, aversive_noise_onset, antic_period_onset, avoid_period_onset, iti_onset, trial_offset, 
            routine.trajectory_description, str(win.nDroppedFrames)]

        f.write("\t".join(output_fields) + "\n")

        # if anything of interest has happened, write to highlights file
        for field in (keyboard_used, keys_pressed, implement_move_direction, target_zigged, touching_target_object, just_made_magic, 
                just_made_first_contact, target_just_exited_catchable_area, aversive_noise_onset, antic_period_onset, avoid_period_onset, iti_onset, trial_offset):
            if field is not "NA" and field is not "0":
                h.write("\t".join(output_fields) + "\n")
                break

    # handling anticipatory phase
    if time_in_trial < antic_period_duration:
        if not routine.started_anticipatory_phase:
            antic_period_onset = '1'
            routine.started_anticipatory_phase = True
        write_to_data_files()
        return

    # handling ITI
    if time_in_trial > antic_period_duration + avoidance_period_duration:
        if not routine.started_ITI:
            routine.stop_all_components()
            routine.start_component(ITI)
            routine.started_ITI = True
            iti_onset = '1'
        elif time_in_trial > antic_period_duration + avoidance_period_duration + ITI_duration:
            routine.live = False
            trial_offset = '1'
        write_to_data_files()
        return

    # reaching this line means that trial is neither in anticipatory nor ITI phase, so implement/target have real positions
    X_target, Y_target = target.pos
    X_implement, Y_implement = implement.pos
    target_zigged = '0'
    keyboard_used = '0'
    target_step = routine.target_step

    # starting up the avoidance phase 
    if not routine.started_avoidance_phase:
        routine.stop_component(antic_background)
        routine.start_component(avoid_background)
        routine.start_component(target)
        routine.start_component(implement)
        routine.started_avoidance_phase = True
        avoid_period_onset = '1'
        send_labjack_event('avoidance_onset')


    # move implement if appropriate (only allowing one movement per frame)
    key_events = event.getKeys()
    if right_key in key_events:
        if implement.pos[0] + implement.size[0]/2 + implement_step_size < screen_width/2:
            implement.pos = (implement.pos[0] + implement_step_size, implement.pos[1])
            implement_move_direction = 'right'
    elif left_key in key_events:
        if implement.pos[0] - implement.size[0]/2 - implement_step_size > -screen_width/2: 
            implement.pos = (implement.pos[0] - implement_step_size, implement.pos[1])
            implement_move_direction = 'left'
    elif up_key in key_events:
        if implement.pos[1] + implement.size[1]/2 + implement_step_size < screen_height/2:
            implement.pos = (implement.pos[0], implement.pos[1] + implement_step_size)
            implement_move_direction = 'up'
    elif down_key in key_events:
        if implement.pos[1] - implement.size[1]/2 - implement_step_size > -screen_height/2:
            implement.pos = (implement.pos[0], implement.pos[1] - implement_step_size)
            implement_move_direction = 'down'

    if len(key_events) >= 1:
        keys_pressed = ','.join(key_events)
        keyboard_used = '1'

    # Popping or cracking target object if it has passed the catchable area and is doomed
    if eval("%d %s %d" %(target.pos[1], boundary_direction, catchable_area_y_boundary)):
        target_outside_catchable_area = '1'
        if not routine.target_has_exited_catchable_area:
            routine.target_has_exited_catchable_area = True
            target_just_exited_catchable_area = '1'
            if routine.target_doomed:
                send_labjack_event("aversive_sound")
                aversive_noise_onset = '1'
                target.setImage(first_break_image)
                routine.time_of_breaking = time_in_trial
                routine.start_component(aversive_sound)
                routine.target_broken = True
            else:
                send_labjack_event("no_aversive_sound")
    else:
        target_outside_catchable_area = '0'

    # changing from pop_1 to pop_2 image after a short period (animation effect)
    if routine.target_broken and time_in_trial > (routine.time_of_breaking + .2):
        target.setImage(second_break_image)

    # moving target if it hasn't popped/cracked
    if not routine.target_broken:
        target.pos = (target.pos[0] + target_step[0], target.pos[1] + target_step[1])
        target.ori = ((target.ori + target_rotation_rate) % 360)
        X_target, Y_target = target.pos
        # reverse x-speed whenever a "zigzag line" is crossed
        if len(routine.zigs) > 0:
            zig_line_position = routine.zigs[0]
            # if within 6 pixels of zigzag line, x-speed reverses (+/- 6 means condition always triggers since max speed is 9)
            if abs(target.pos[0] - zig_line_position) < 6:
                routine.target_step = (-target_step[0], target_step[1])
                routine.zigs.pop(0)
                target_zigged = '1'


    # measuring distance between implement and target object
    x_dist = int(implement.pos[0] - target.pos[0])
    y_dist = int(implement.pos[1] - target.pos[1])

    # testing if the current x/y distance between target and implement should be counted as a collision
    if y_dist in collision_space_by_y and x_dist >= collision_space_by_y[y_dist][0] and x_dist <= collision_space_by_y[y_dist][1]:
        touching_target_object = '1'
        # Various events occur if this is the first time in the trial that the target has been touched
        if not routine.target_broken and not routine.target_has_been_touched:
            routine.target_has_been_touched = True
            send_labjack_event("first_contact")
            just_made_first_contact = '1'
            # in the controllable stress condition (balloon game), making touching balloon (with wand or hand) prevents it from popping
            if mode == cs:
                routine.target_doomed = False
            # start magic sound and iterate spells cast count if playing magic game
            if playing_magic_game:
                routine.time_of_magic = time_in_trial
                routine.magic_has_happened = True
                global spells_cast
                spells_cast += 1 
                counter.setText("Spells cast: %d" % spells_cast)
                routine.start_component(magic_sound)
                #routine.magic_has_happened = True
                just_made_magic = '1'
                if playing_egg_game:
                    target.setColor(choice(("INDIANRED", "GOLD", "YELLOWGREEN", "DEEPSKYBLUE"))) # random.choice picks an element from a list randomly
                else:
                    routine.start_component(magic_sparks)
    else:
        touching_target_object = '0'

    # handle magic sparks if magic game is being played
    if playing_magic_game:
        # move the sparks with the target object (it's okay if the component isn't being drawn yet)
        magic_sparks.pos = (target.pos[0] + sparks_balloon_offset_x, target.pos[1] + sparks_balloon_offset_y)

        # stop the magic sparks after a reasonable period
        if routine.magic_has_happened and time_in_trial > routine.time_of_magic + magic_sparks_duration:
            routine.stop_component(magic_sparks)
    write_to_data_files()

# at the end of each trial for the balloon_cs mode, need to preserve the order of pops/non-pops
def trial_shutdown(routine):
    if mode == cs:
        global aversive_sound_by_trial_num
        aversive_sound_by_trial_num[current_trial_num] = routine.target_broken # for readability, would be better to have a variable called sound_has_played
    elif playing_egg_game:
        # only way found so far to reset a color change!
        global target
        target = visual.ImageStim(win = win, name = 'egg', units = 'pix', image = whole_egg_image, interpolate = True, depth = -3.0)
# build a list of routines to run
routines = []
instructions_1 = Routine(window = win, run_frame = lambda routine: run_slides(routine, 1, 14))
implement_practice = Routine(window = win, startup = implement_practice_startup, run_frame = implement_practice_run_frame)
instructions_2 = Routine(window = win, run_frame = lambda routine: run_slides(routine, 15, 17))

if not skip_instructions: routines.extend((instructions_1, implement_practice, instructions_2))

# add all the trial routines to the list of routines
for trial_num in range(1, num_trials + 1):
    # if debugging one trial, skip the other trials
    if trial_debug_mode and trial_num != debug_trial:
        if trial_num < debug_trial:
            current_trial_num += 1
        continue
    trial = Routine(window = win, startup = trial_startup, run_frame = trial_run_frame, shutdown = trial_shutdown)
    routines.append(trial)

thanks = Routine(window = win, run_frame = lambda routine: run_slides(routine, 18, 18))
routines.append(thanks)


# Now that the experiment is about to run, write data file headers
for handle in (f, h):
    handle.write("# Version: %s\n" % version)
    handle.write("# Task type: %s\n" % game_type)
    handle.write("# Task mode: %s\n" % mode)
    if mode == us:
        handle.write("# Yoking file: %s\n" % yoke_source) 
    handle.write("Participant_ID\ttrial_num\ttimestamp\ttime_of_day_in_seconds\ttime_in_trial\tX_target\tY_target\tX_implement\tY_implement\tkeyboard_used\tkeys_pressed\t" +
        "implement_move_direction\ttarget_zigged\ttouching_target_object\ttarget_outside_catchable_area\tjust_made_magic\tjust_made_first_contact\ttarget_just_exited_catchable_area\taversive_noise_onset\tantic_period_onset\t" +
        "avoid_period_onset\titi_onset\ttrial_offset\ttrial_trajectory\ttotal_frames_dropped\n")

# Run all routines
for routine in routines:
    Routine.run_routine(routine)

## Wrap things up

# Close output files and compress the full output file (which may never be needed, anyway)
f.close()
h.close()
call("gzip %s" % full_data_file, shell = True)

# Record aversive sound outcomes from cs condition for future yoked runs
if mode == cs:
    yoking_file = "%s/yoking_file.pickle" % output_dir
    with open (yoking_file, 'w') as y:
        pickle.dump(aversive_sound_by_trial_num, y)
print "Finished the game!"
print "Output has been written to %s." % output_dir

# Psychopy shutdown code
this_exp.saveAsPickle(exp_handler_log)
logging.flush()
this_exp.abort()
win.close()
core.quit()
