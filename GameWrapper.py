import sys
import os
import re
import datetime
import signal
from subprocess import call, check_output

# make it pretty when user quits with Control-C
def catch_sigint(signal, frame):
	print "\nThe user has aborted the script."
	sys.exit()
signal.signal(signal.SIGINT, catch_sigint)

# This script should not be moved from its location in the sc task directory
source_dir = os.path.dirname(os.path.abspath(__file__))

# Read the local config file
config_file = source_dir + '/local_config'

try:
	config = open(config_file, 'r')
except IOError as e:
	print "Error: Could not open local config file. Have you followed the installation instructions?"
	sys.exit()
except:
	raise

for line in config:
	line = line.strip()
	if line.startswith('#'): continue
	elif re.search('^output_directory=', line):
		output_directory = re.sub('^output_directory=', '', line)
		if not os.path.exists(output_directory):
			print "Error: Output directory %s given in local config file does not exist." % output_directory
			sys.exit()
		else:
			output_directory = os.path.abspath(output_directory)
	elif re.search('^test_directory=', line):
		test_directory = re.sub('^test_directory=', '', line)
		if not os.path.exists(test_directory):
			print "Error: Test directory %s given in local config file does not exist." % test_directory
			sys.exit()
		else:
			output_directory = os.path.abspath(output_directory)
	elif re.search('^python_bin=', line):
		python_bin = re.sub('^python_bin=', '', line)

# ensure all necessary local settings are declared in local_config file
try:
	for req in ["output_directory", "python_bin", "test_directory"]: eval(req)
except NameError:
	print "Error: %s not declared in local_config file" % req
	sys.exit()

balloon_game_info = {
	'LongName':"Balloon Game (Controllable stress, uncontrollable stress, or non-stressed)",
	'ShortName':"Balloon Game",
	'DirName': "BalloonGame",
	'Script':"%s/task_code/BalloonGame.py" % source_dir,
}

egg_game_info = {
	'LongName': "Egg Game (T2 uncontrollable stress)",
	'ShortName': "Egg Game",
	'DirName': "EggGame",
	'Script': "%s/task_code/EggGame.py" % source_dir,
}

noise_rating_info = {
	'LongName': "Noise Rating",
	'ShortName': "Noise Rating Game",
	'DirName': "NoiseRating",
	'Script': "%s/task_code/NoiseRating.py" % source_dir,
}

# making sure that the scripts/media files that will be used match the current commit
# this would all need to be changed if the folder structure changed
change_list = (check_output("git -C %s status --porcelain" % source_dir, shell=True).split("\n"))
source_clean = True
for line in  change_list:
	if re.search(os.path.basename(__file__), line):
		source_clean = False
	if re.search("sc_media", line):
		source_clean = False
	if re.search("task_code", line):
		source_clean = False

# Making sure project code hasn't been altered accidentally
version = "unknown"
if source_clean:
	version = check_output("git -C %s rev-parse --short HEAD" % source_dir, shell=True).strip()
else:
	print "Warning: The project source directory has been altered from the last commit."
	print "Unless you know what you're doing, you should pull the source code from Bitbucket before continuing."
	print "Here's a list of the changes:"
	for line in change_list: print line
	to_continue = raw_input("\nWould you like to continue (y/n)? ")
	while True:
		if to_continue == 'n':
			sys.exit()
		if to_continue == 'y': break
		to_continue = raw_input("Invalid response. Choose \"y\" to continue or \"n\" to quit: ")

game_options = (balloon_game_info, egg_game_info, noise_rating_info)
num_games = len(game_options)

# prompt user to pick game
print "Here are the available games:"
for x in range(num_games):
	print str(x+1) + ") " + game_options[x]['LongName']

choice = raw_input("Which game should be played? ")
while True:
	try:
		chosen_game_info = game_options[int(choice) - 1]
		break
	except:
		choice = raw_input("Invalid input. Enter a choice from %d-%d: " %(1, num_games))

print "All right, we're playing the %s!" %(chosen_game_info['ShortName'])

# See if this is a real experiment or a test run
run_type = "Real Experiment"
choice = raw_input("Is this going to be...\n1) A test run or 2) The real thing? ")
while True:
	try:
		if int(choice) == 1:
			output_directory = test_directory
			run_type = "Test Run"
			break
		elif int(choice) == 2:
			break
	except:
		choice = raw_input("Invalid input. Enter 1 for a test run, or 2 for a real experiment: ")

test_options = '' # will be passed on command line to the game script
if run_type == "Test Run":
	print "\nTesting options:\n1) Full run\n2) Skip instructions\n3) Short ITI\n4) Skip instructions AND short ITI\n5) Test specific trial\n"
	choice = raw_input("Which test should be run? ")
	while True:
		try:
			if int(choice) == 1:
				break
			elif int(choice) == 2:
				test_options = "--skip-instructions"
				break
			elif int(choice) == 3:
				test_options = "--short-iti"
				break
			elif int(choice) == 4:
				test_options = "--skip-instructions --short-iti"
				break
			elif int(choice) == 5:
				trial_to_test = raw_input("Which trial number should be tested? ")
				while True:
					try:
						int(trial_to_test) # ensuring conversion to integer is possible
						print "Okay, we'll test trial %s." % trial_to_test
						test_options = "--debug-trial %s" % trial_to_test
						break
					except:
						trial_to_test = raw_input("Invalid response. Input the numberical position of the trial to test: ")
				break
			else: raise
		except:
			choice = raw_input("Invalid response. Enter the number corresponding to the type of test to run: ")

# Create game-specific output directory if needed
output_directory += "/%s" %chosen_game_info['DirName']
if not os.path.exists(output_directory): os.mkdir(output_directory)

# A couple of balloon-game-specific variables
yoking_source_file = ''
is_boring = False

if chosen_game_info['ShortName'] is 'Balloon Game':
	# yoking files will always be stored in balloon game output directory
	yoking_file_dir = output_directory + "/yoking_files"
	if not os.path.exists(yoking_file_dir):
		os.makedirs(yoking_file_dir)
		print "Note: Your chosen output directory (%s) did not have a pre-existing subdirectory for yoking files," % output_directory
		print 'so one was just created (%s).' % yoking_file_dir
	current_participant_is_yoked = False
	
	stress_type = raw_input("Should the game be played with 1) controllable stress, 2) uncontrollable stress (yoked), or 3) non-stressed (yoked)? ")
	while True:
		if stress_type == "1":
			stress_type = "controllable"
			print "Okay, the game will be played with controllable stress."
			break
		if stress_type == "2":
			stress_type = "uncontrollable"
			print "Okay, the game will be played with uncontrollable stress."
		elif stress_type == "3":
			stress_type = "non-stressed"
			print "Okay, the game will be played with no stress."
			is_boring = True
		if stress_type == "uncontrollable" or stress_type == "non-stressed":
			current_participant_is_yoked = True
			print "Here is a list of previous participants from the controllable stress condition:"
			yoking_files = os.listdir(yoking_file_dir)
			numYokingFiles = 0
			for f in yoking_files:
				numYokingFiles += 1
				print "%d) %s" %(numYokingFiles, f)
			chosenNum = raw_input("Which existing yoking source file from a previous participant should be used (1-%d)? " %(numYokingFiles))
			while True:
				try:
					assert int(chosenNum) > 0 and int(chosenNum) <= numYokingFiles
					yoking_source_file = yoking_files[int(chosenNum) - 1]
					print "Okay, the current file will be yoked to this participant: %s." %(yoking_source_file)
					break
				except:
					chosenNum = raw_input("Invalid response. Choose a yoking source file from 1-%d: " %(numYokingFiles))
			break
		stress_type = raw_input("Invalid response. Enter 1 for controllable stress, 2 for uncontrollable stress, 3 for non-stressed: ")
	
participant_id = 'Missing'
new_id = raw_input("Assign an ID for the new participant: ")
while True:
	pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
	if re.search(pattern, new_id):
		participant_id = new_id
		print "Okay, the current participant has been assigned the ID %s." %(participant_id)
		break
	new_id = raw_input("Invalid ID. Legal characters are letters, numbers, hyphens, and underscores. Choose a new ID: ")


button_box_mode = False
if chosen_game_info['ShortName'] is 'Balloon Game' or chosen_game_info['ShortName'] is 'Egg Game':
	response = raw_input("Are we playing with 1) keyboard input or 2) button box input? ")
	while True:
		try:
			response = int(response)
		except ValueError:
			response = raw_input("Invalid response. Enter 1 for keyboard input mode, or 2 for button box input: ")
			continue
		if response == 1:
			print "Okay, we'll play with keyboard input."
			break
		elif response == 2:
			print "Okay, we'll play with button box input."
			button_box_mode = True
			break
		else:
			response = raw_input("Invalid response. Enter 1 for keyboard input mode, or 2 for button box input: ")
	


print "\nHere are the options that have been chosen: "
print "Game: %s" %(chosen_game_info['ShortName'])
print "Run type: %s" % run_type
print "Participant ID: %s" %(participant_id)
input_mode = "button box" if button_box_mode else "keyboard"
if chosen_game_info['ShortName'] == 'Balloon Game' or chosen_game_info['ShortName'] == 'Egg Game':
	print "Input mode: %s" % input_mode
if chosen_game_info['ShortName'] == 'Balloon Game':
	print "Stress type: %s" %(stress_type)
	if current_participant_is_yoked:
		print "Participant yoked to this file: %s" % yoking_source_file
		yoking_source_file = "%s/%s" %(yoking_file_dir, yoking_source_file)
	else:
		print "Create a yoking file for future use here: %s" % yoking_file_dir
print "Save output here: %s" % output_directory
confirm = raw_input("\nDoes everything look okay to run (y/n)? ")
while True:
	if confirm == 'y':
		print "Okay. Running now!"
		break;
	if confirm == 'n':
		print "Aborting. No game will be played!"
		sys.exit()
	confirm = raw_input("Invalid response. Choose \"y\" to confirm or \"n\" to quit: ")

timestamp = '{:%Y-%b-%d_%H:%M:%S}'.format(datetime.datetime.now())
# all three scripts require the arguments given with "--id", "--source_dir", and "--output_dir"
script_with_args = python_bin + " '%s' --source=%s --output=%s --id=%s --version=%s %s" %(chosen_game_info['Script'], source_dir, output_directory, participant_id, version, test_options)
if yoking_source_file: script_with_args += " --yoke_source=%s" % yoking_source_file
if is_boring: script_with_args += " --boring_mode"
if button_box_mode: script_with_args += " --button_box"
print "Running this: %s" % script_with_args
call(script_with_args, shell=True)
