import sys
import os
import re
import datetime
from subprocess import call


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
			print "Error: Output directory %s given in local config file does not exist." %output_directory
			sys.exit()
		else:
			output_directory = os.path.abspath(output_directory)
	elif re.search('^python_bin=', line):
		python_bin = re.sub('^python_bin=', '', line)


if not output_directory:
	print "Error: output_directory not declared in local_config file."
	sys.exit()
if not python_bin:
	print "Error: python_bin not declared in local_config file."
	sys.exit()


balloon_game_info = {
	'LongName':"Balloon Game (Controllable stress, uncontrollable stress, or non-stressed)",
	'ShortName':"Balloon Game",
	'DirName': "BalloonGame",
	'Script':"%s/task_code/BalloonGame.py" % source_dir,
}

egg_game_info = {
	'LongName':"Egg Game (T2 uncontrollable stress)",
	'ShortName':"Egg Game",
	'DirName': "EggGame",
	'Script':"%s/task_code/EggGame.py" % source_dir,
}


# yoking files will always be stored in balloon game output directory
yoking_file_dir = output_directory + "/%s/yoking_files" % balloon_game_info['DirName']
if not os.path.exists(yoking_file_dir):
	os.makedirs(yoking_file_dir)
	print "Note: Your chosen output directory (%s) did not have a pre-existing subdirectory for yoking files," % output_directory
	print 'so one was just created (%s).' % yoking_file_dir


current_participant_is_yoked = False
yoking_source_file = ''
is_boring = False # indicates if the "boring" (non-stressed) version of the game is being played
game_options = (balloon_game_info, egg_game_info)
num_games = len(game_options)

# prompt user to pick game
print "Here are the available games:"
for x in range(num_games):
	print str(x+1) + ") " + game_options[x]['LongName']

choice = raw_input("Which game should be played? ")
while True:
	try:
		chosen_game_info =  game_options[int(choice) - 1]
		break
	except:
		choice = raw_input("Invalid input. Enter a choice from %d-%d: " %(1, num_games))

print "All right, we're playing the %s!" %(chosen_game_info['ShortName'])
output_directory += "/%s" %chosen_game_info['DirName']
if not os.path.exists(output_directory): os.mkdir(output_directory)

if chosen_game_info['ShortName'] is 'Balloon Game':
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

print "\nHere are the options that have been chosen: "
print "Game: %s" %(chosen_game_info['ShortName'])
print "Participant ID: %s" %(participant_id)
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
psychopy_log_name = "%s/%s-%s-%s" % (output_directory, chosen_game_info['DirName'], participant_id, timestamp)
script_with_args = python_bin + " '%s' --source=%s --output=%s --id=%s" %(chosen_game_info['Script'], source_dir, output_directory, participant_id)
if yoking_source_file: script_with_args += " --yoke_source=%s" % yoking_source_file
if is_boring: script_with_args += " --boring_mode"
script_with_args += " %s" % psychopy_log_name
print "Running this: %s" % script_with_args
call(script_with_args, shell=True)
