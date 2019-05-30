#!/usr/bin/env python3
import sys, os
import re, datetime, signal
from subprocess import call, check_output

# make it pretty when user quits with Control-C
def catch_sigint(signal, frame):
	print("\nThe user has aborted the script.")
	sys.exit()
signal.signal(signal.SIGINT, catch_sigint)

# This script should not be moved from its location in the sc task directory
source_dir = os.path.dirname(os.path.abspath(__file__))

# Read the local config file
config_file = source_dir + '/local_config'

try:
	config = open(config_file, 'r')
except IOError as e:
	print("Error: Could not open local config file. Have you followed the installation instructions?")
	sys.exit()
except:
	raise

for line in config:
	line = line.strip()
	if line.startswith('#'): continue
	elif re.search('^magic_output_directory=', line):
		magic_output_directory = re.sub('^magic_output_directory=', '', line)
		if not os.path.exists(magic_output_directory):
			print("Error: Output directory %s given in local config file does not exist." % magic_output_directory)
			sys.exit()
		else:
			magic_output_directory = os.path.abspath(magic_output_directory)
	elif re.search('^mundane_output_directory=', line):
		mundane_output_directory = re.sub('^mundane_output_directory=', '', line)
		if not os.path.exists(mundane_output_directory):
			print("Error: Output directory %s given in local config file does not exist." % mundane_output_directory)
			sys.exit()
		else:
			mundane_output_directory = os.path.abspath(mundane_output_directory)	
	elif re.search('^test_directory=', line):
		test_directory = re.sub('^test_directory=', '', line)
		if not os.path.exists(test_directory):
			print("Error: Test directory %s given in local config file does not exist." % test_directory)
			sys.exit()
		else:
				test_directory = os.path.abspath(test_directory)

# ensure all necessary local settings are declared in local_config file
try:
	for req in ("magic_output_directory", "mundane_output_directory", "test_directory"):
		eval(req)
except NameError:
	print("Error: %s not declared in local_config file" % req)
	sys.exit()

balloon_game_info = {
	'LongName':"Balloon Game (Controllable stress, uncontrollable stress, or non-stressed)",
	'ShortName':"Balloon",
	'Script':"%s/sc_games.py" % source_dir,
}

noise_rating_info = {
	'LongName':"Noise Rating Task",
	'ShortName':"Noise Rating",
	'Script':"%s/noise_rating.py" % source_dir,
}

egg_game_info = {
	'LongName': 'Egg Game (T2)',
	'ShortName': 'Egg',
	'Script':"%s/sc_games.py" % source_dir
}

balloon = balloon_game_info['ShortName']
noise_rating = noise_rating_info['ShortName']
egg = egg_game_info['ShortName']

# making sure that the scripts/media files that will be used match the current commit
# this would all need to be changed if the folder structure changed
change_list = (check_output("git -C %s status --porcelain" % source_dir, shell=True, encoding='utf-8').split("\n"))
source_clean = True
for line in change_list:
	if re.search(os.path.basename(__file__), line):
		source_clean = False
	if re.search("media", line):
		source_clean = False
	if re.search("sc_games", line):
		source_clean = False
	if re.search("noise_rating", line):
		source_clean = False

# Making sure project code hasn't been altered accidentally
version = "unknown"
if source_clean:
	version = check_output("git -C %s rev-parse --short HEAD" % source_dir, shell=True, encoding='utf-8').strip()
else:
	print("Warning: The project source directory has been altered since the last commit.")
	print("Unless you know what you're doing, you should discard local changes and pull the source code from Bitbucket before continuing.")
	print("Here's a list of the changes:")
	for line in change_list: print(line)
	to_continue = input("\nWould you like to continue (y/n)? ")
	while True:
		if to_continue == 'n':
			sys.exit()
		if to_continue == 'y': break
		to_continue = input("Invalid response. Choose \"y\" to continue or \"n\" to quit: ")

exp_options = (("Magic (with wand)", "magic"), ("Mundane (with hand)", "mundane"))
num_exps = len(exp_options)

print("Here are the experiments that can be run:")
for x in range(num_exps):
	print(str(x+1) + ") " + exp_options[x][0])

exp_choice = input("Which experiment should be run? ")
while True:
	try:
		exp_type = exp_options[int(exp_choice) - 1][1]
		exp_name = exp_options[int(exp_choice) - 1][0]
		break
	except:
		choice = input("Invalid response. Enter the number (1-%d) corresponding to the experiment to run: " % num_exps)
print("Okay, we're running the \"%s\" experiment!" % exp_name)

task_options = (balloon_game_info, egg_game_info, noise_rating_info)
num_tasks = len(task_options)
# prompt user to pick task
print("Here are the available activities:")
for x in range(num_tasks):
	print(str(x+1) + ") " + task_options[x]['LongName'])

task_choice = input("Which task should be run? ")
while True:
	try:
		chosen_task_info = task_options[int(task_choice) - 1]
		break
	except:
		task_choice = input("Invalid input. Enter a choice from %d-%d: " %(1, num_tasks))

game_chosen = chosen_task_info['ShortName']
print("All right, we're running the %s task!" % game_chosen)

# See if this is a real experiment or a test run
run_type = "Real Experiment"
choice = input("Is this going to be...\n1) A test run or 2) The real thing? ")
while True:
	try:
		if int(choice) == 1:
			output_directory = test_directory
			run_type = "Test Run"
			break
		elif int(choice) == 2:
			output_directory = magic_output_directory if exp_type == "magic" else mundane_output_directory
			break
	except:
		choice = input("Invalid input. Enter 1 for a test run, or 2 for a real experiment: ")

test_options = '' # will be passed on command line to the game script

participant_id = input("Assign an ID for the new participant: ")
while True:
	pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
	if re.search(pattern, participant_id):
		print("Okay, the current participant is %s." % participant_id)
		break
	participant_id = input("Invalid ID. Legal characters are letters, numbers, hyphens, and underscores. Choose a new ID: ")

debug_trial_mode = False
if game_chosen is not noise_rating:	
	if run_type == "Test Run":
		print("\nTesting options:\n1) Full run\n2) Skip instructions\n3) Fast mode (short ITI/anticipatory periods)\n4) Skip instructions AND fast mode\n5) Test specific trial\n")
		choice = input("Which test should be run? ")
		while True:
			try:
				if int(choice) == 1:
					break
				elif int(choice) == 2:
					test_options = "--skip-instructions --free-volume"
					break
				elif int(choice) == 3:
					test_options = "--fast --free-volume"
					break
				elif int(choice) == 4:
					test_options = "--skip-instructions --fast --free-volume"
					break
				elif int(choice) == 5:
					trial_to_test = input("Which trial number should be tested? ")
					debug_trial_mode = True
					while True:
						try:
							int(trial_to_test) # ensuring conversion to integer is possible
							print("Okay, we'll test trial %s." % trial_to_test)
							test_options = "--debug-trial %s" % trial_to_test
							break
						except:
							trial_to_test = input("Invalid response. Input the numberical position of the trial to test: ")
					break
				else: raise
			except:
				choice = input("Invalid response. Enter the number corresponding to the type of test to run: ")


	# Ask which balloon game version to play (cs, us, ns)
	if game_chosen is balloon:
		stress_type = input("Should the game be played with 1) controllable stress, 2) uncontrollable stress (yoked), or 3) non-stressed? ")
		current_participant_is_yoked = False
		while True:
			if stress_type == "1":
				game_mode = "balloon_cs"
				stress_condition = "controllable"
				print("Okay, the game will be played with controllable stress.")
				break
			if stress_type == "2":
				game_mode = "balloon_us"
				stress_condition = "uncontrollable"
				print("Okay, the game will be played with uncontrollable stress.")
			elif stress_type == "3":
				game_mode = "balloon_ns"
				stress_condition = "nonstressed"
				print("Okay, the game will be played with no stress.")
				break
			if game_mode == "balloon_us":
				current_participant_is_yoked = True
				print("Here is a list of previous participants from the controllable stress condition:")
				yoking_files = check_output("find %s -name 'yoking_file.pickle'" % output_directory, shell=True, encoding='utf-8').split("\n")
				num_yoking_files = 0
				yokeable_subject = ''
				for f in yoking_files:
					if f == '':
						continue
					num_yoking_files += 1
					yokeable_subject = os.path.dirname(f)
					yokeable_subject = re.sub("%s\/?" % output_directory, '', yokeable_subject)
					print("%d) %s" %(num_yoking_files, yokeable_subject))

				if num_yoking_files == 0:
					print("\nNo yoking files found for the given experiment type in %s." % output_directory)
					print("Either no controllable stress conditions have been run, the output files have been moved, they were generated")
					print("on another computer and haven't synched, or the output directory settings in your local_config file should be")
					print("changed to reflect the actual location of the yoking files. Alternatively, if you know which yoking file")
					print("you would like to use, you could run the game script directly instead of using this wrapper.")
					sys.exit()
				chosenNum = input("Which existing yoking source file from a previous participant should be used (1-%d)? " % (num_yoking_files))
				while True:
					try:
						assert int(chosenNum) > 0 and int(chosenNum) <= num_yoking_files
						yoking_source_file = yoking_files[int(chosenNum) - 1]
						print("Okay, this yoking file will be used: %s." % yoking_source_file)
						break
					except:
						chosenNum = input("Invalid response. Choose a yoking source file from 1-%d: " %(num_yoking_files))
				break
			stress_type = input("Invalid response. Enter 1 for controllable stress, 2 for uncontrollable stress, 3 for non-stressed: ")
	elif game_chosen is egg:
		game_mode = "egg"

	# Prompt for randomization mode
	non_randomized = True
	# if not debug_trial_mode:
	# 	response = input("Should trial presentation order be 1) randomized or 2) non-randomized? ")
	# 	while True:
	# 		try:
	# 			response = int(response)
	# 		except ValueError:
	# 			response = input("Invalid response: Enter 1 for randomized trial order, or 2 for non-randomized: ")
	# 			continue
	# 		if response == 1:
	# 			print("Okay. Trial presentation order will be randomized.")
	# 			break
	# 		if response == 2:
	# 			print("Okay. Trial presentation order will NOT be randomized.")
	# 			non_randomized = True
	# 			break
	# 		else:
	# 			response = input("Invalid response: Enter 1 for randomized trial order, or 2 for non-randomized: ")
	# else:
	# 	non_randomized = True

	# Prompt for keyboard input mode vs. button box mode
	mri_mode = False
	response = input("Are we playing with 1) keyboard input or 2) button box input (MRI mode)? ")
	while True:
		try:
			response = int(response)
		except ValueError:
			response = input("Invalid response. Enter 1 for keyboard input mode, or 2 for button box input (MRI mode): ")
			continue
		if response == 1:
			print("Okay, we'll play with keyboard input.")
			break
		elif response == 2:
			print("Okay, we'll play in MRI mode (button box input, MRI trigger, two phases of trials).")
			mri_mode = True
			break
		else:
			response = input("Invalid response. Enter 1 for keyboard input mode, or 2 for button box input (MRI mode): ")
	
print("\nHere are the options that have been chosen: ")
print("Experiment: %s" % exp_name)
print("Mode: %s" % chosen_task_info['ShortName'])
print("Run type: %s" % run_type)
print("Participant ID: %s" % participant_id)
if game_chosen is not noise_rating:
	if game_chosen is balloon:
		print("Stress type: %s" %(stress_condition))
		if current_participant_is_yoked:
			print("Participant yoked to this file: %s" % yoking_source_file)
	randomization_mode = "non-random" if non_randomized else "random"
	print("Trial presentation order: %s" % randomization_mode)
	input_mode = "button box (MRI mode)" if mri_mode else "keyboard"
	print("Input mode: %s" % input_mode)
print("Save output here: %s" % output_directory)

confirm = input("\nDoes everything look okay to run (y/n)? ")
while True:
	if confirm == 'y':
		break;
	if confirm == 'n':
		print("Aborting. No game will be played!")
		sys.exit()
	confirm = input("Invalid response. Choose \"y\" to confirm or \"n\" to quit: ")

# all three scripts require the arguments given with "--id", "--source_dir", and "--output_dir"
script_with_args = "python '%s' --participant-id=%s  --output=%s  --version=%s" %(chosen_task_info['Script'], participant_id, output_directory, version)
if chosen_task_info['ShortName'] is not 'Noise Rating':
	script_with_args += " --game-type=%s --game-mode=%s %s" % (exp_type, game_mode, test_options)
	if game_chosen is balloon and current_participant_is_yoked: script_with_args += " --yoke-source=%s" % yoking_source_file
	if mri_mode: script_with_args += " --mri-mode"
	if non_randomized: script_with_args += " --non-randomized"

print("Make sure you've activated the sc python environment, and run this:")
print(script_with_args)
