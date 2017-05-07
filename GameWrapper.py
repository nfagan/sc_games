import sys
import os
import re
from subprocess import call

# edit this if changing to a new enviornment
sourceDir = "/Users/ecohodes/Dropbox/sc"

# edit the python path to point to the python version that has Psychopy installed
pythonBin = "/usr/bin/python";


yokingFileDir = sourceDir + "/yoking_files"
currentParticipantIsYoked = False
yokingSourceFile = ''

balloonGameInfo = {
	'LongName':"Balloon Game (Controllable stress, uncontrollable stress, or non-stressed)",
	'ShortName':"Balloon Game",
	'Script':"%s/Balloon Game/BalloonGame.py"%(sourceDir),
}

eggGameInfo = {
	'LongName':"Egg Game (T2 uncontrollable stress)",
	'ShortName':"Egg Game",
	'Script':"%s/Egg Game/EggGame.py"%(sourceDir),
}



isBoring = "0" # indicates if the "boring" (non-stressed) version of the game is being played
gameOptions = (balloonGameInfo, eggGameInfo)
numGames = len(gameOptions)
print "Here are the available games:"
for x in range(numGames):
	print str(x+1) + ") " + gameOptions[x]['LongName']

choice = raw_input("Which game should be played? ")
while True:
	try:
		chosenGameInfo =  gameOptions[int(choice) - 1]
		break
	except:
		choice = raw_input("Invalid input. Enter a choice from %d-%d: " %(1, numGames))

print "All right, we're playing the %s!" %(chosenGameInfo['ShortName'])

if chosenGameInfo['ShortName'] is 'Balloon Game':
	stressType = raw_input("Should the game be played with 1) controllable stress, 2) uncontrollable stress (yoked), or 3) non-stressed (yoked)? ")
	while True:
		if stressType == "1":
			stressType = "controllable"
			print "Okay, the game will be played with controllable stress."
			break
		if stressType == "2":
			stressType = "uncontrollable"
			print "Okay, the game will be played with uncontrollable stress."
		elif stressType == "3":
			stressType = "non-stressed"
			print "Okay, the game will be played with no stress."
			isBoring = "1"
		if stressType == "uncontrollable" or stressType == "non-stressed":
			currentParticipantIsYoked = True
			print "Here is a list of previous participants from the controllable stress condition:"
			yokingFiles = os.listdir(yokingFileDir)
			numYokingFiles = 0
			for f in yokingFiles:
				numYokingFiles += 1
				print "%d) %s" %(numYokingFiles, f)
			chosenNum = raw_input("Which existing yoking source file from a previous participant should be used (1-%d)? " %(numYokingFiles))
			while True:
				try:
					assert int(chosenNum) > 0 and int(chosenNum) <= numYokingFiles
					yokingSourceFile = yokingFiles[int(chosenNum) - 1]
					print "Okay, the current file will be yoked to this participant: %s." %(yokingSourceFile)
					break
				except:
					chosenNum = raw_input("Invalid response. Choose a yoking source file from 1-%d: " %(numYokingFiles))
			break
		stressType = raw_input("Invalid response. Enter 1 for controllable stress, 2 for uncontrollable stress, 3 for non-stressed: ")
	
participantID = 'Missing'
newID = raw_input("Assign an ID for the new participant: ")
while True:
	pattern = '^[A-Za-z0-9][A-Za-z0-9_\-]*$'
	if re.search(pattern, newID):
		participantID = newID
		print "Okay, the current participant has been assigned the ID %s." %(participantID)
		break
	newID = raw_input("Invalid ID. Legal characters are letters, numbers, hyphens, and underscores. Choose a new ID: ")

print "\nHere are the options that have been chosen: "
print "Game: %s" %(chosenGameInfo['ShortName'])
print "Participant ID: %s" %(participantID)
if chosenGameInfo['ShortName'] == 'Balloon Game':
	print "Stress type: %s" %(stressType)
	if currentParticipantIsYoked:
		print "Participant yoked to this file: %s" %(yokingSourceFile)
		yokingSourceFile = "%s/%s" %(yokingFileDir, yokingSourceFile)
confirm = raw_input("\nDoes everything look okay to run (y/n)? ")
while True:
	if confirm == 'y':
		print "Okay. Running now!"
		break;
	if confirm == 'n':
		print "Aborting. No game will be played!"
		sys.exit()
	confirm = raw_input("Invalid response. Choose \"y\" to confirm or \"n\" to quit: ")

call(pythonBin + " '%s' %s %s %s" %(chosenGameInfo['Script'], participantID, yokingSourceFile, isBoring), shell=True)
