#!/usr/bin/env python2
import os, sys
from optparse import OptionParser
from datetime import datetime as dt
import math
import re

# This script takes in a timestamp from the acquistion software (which, along with a "lag" factor, tells when GSR acquisition started)
# and then creates a list of relevant task events with time given in terms of seconds since start of acquisition
# The output list is in a specific format that is designed for importing as an event list into the GSR software

def main():
	# declare input arguments
	parser = OptionParser()
	parser.add_option("-i", "--input", metavar="INPUT", dest="inputFile", help="The Psychopy task output file")
	parser.add_option("-o", "--output", metavar="OUTPUT", dest="outputFile", help="The name for the event list produced by this script")
	parser.add_option("-t", "--timestamp", metavar="ACQ_TIMESTAMP", dest="acqTimestamp", help="A timestamp from Acqknowledge, given in quotes")
	parser.add_option("-l", "--lag", metavar="LAG", dest="timestampLag", type="int", help="The rounded number of seconds from start of acquisition until timestamp")
	(options, args) = parser.parse_args()
	inputFile = options.inputFile
	outputFile = options.outputFile
	rawAcqTimestamp = options.acqTimestamp
	lag = options.timestampLag

	# ensure required arguments are supplied, that files exist, etc.
	if not inputFile or not outputFile or not rawAcqTimestamp or (not lag and lag != 0) or len(args) != 0:
		parser.print_help()
		sys.exit()

	if not os.path.isfile(inputFile):
		print "Error: The input file \"%s\" does not exist." % inputFile
		sys.exit()
	else:
		inputFile = os.path.abspath(inputFile)

	if os.path.isfile(outputFile):
		print "Error: There is already a file called \"%s\"." % outputFile
		sys.exit()

	try:
		# convert input timestamp into a datetime object
		startTime = dt.strptime(rawAcqTimestamp, "%B %d %Y %H:%M:%S")
		startTime = startTime.replace(second = startTime.second - lag) # subtracting the offset
		print "Acquisition started at approximately {}".format(startTime)
	except:
		print "Error: Failed to determine acquisition start time from input timestamp/lag values.\n"
		print "Make sure the timestamp is in this format: April 09 2017 18:29:01\n";
		sys.exit()

	try:
		f = open(inputFile, 'U')
	except:
		print "Error: Could not open input file \"%s\"." % inputFile

	try:
		w = open(outputFile, 'w')
	except:
		print "Error: Could not create output file \"%s\"." %outputFile

	f.readline() # skipping header
	w.write("time\tnid\tdescription\n") # this is the format required by the gsr software for importing events

	# read through task output file and convert timestamps for relevant events
	currentTrial = 0
	nid = 0
	for line in f:
		fields = line.rstrip().split("\t")
		event_time_left = re.sub("\..*", '', fields[1])
		event_time_right = re.sub(".*\.", '.', fields[1])
		event_time_right = round(float(event_time_right), 6)
		event_time_right = re.sub('^0.', '.', str(event_time_right))
		while len(event_time_right) != 7: event_time_right += '0'
		unconverted_event_time = event_time_left + event_time_right
		event_time = dt.strptime(unconverted_event_time, '%Y-%m-%d %H:%M:%S.%f')
		currentTrialClock = float(fields[3])
		time_since_start = (event_time - startTime).total_seconds()
		trial = int(fields[2])
		poppedBalloon = int(fields[12])
		savedBalloon = int(fields[13])
		x_balloon, y_balloon, x_hand, y_hand = fields[4], fields[5], fields[6], fields[7]
		xDist = abs(float(x_hand) - float(x_balloon))
		yDist = abs(float(y_hand) - float(y_balloon))
		event_type = "other"
		should_have_caught = True if (xDist < .05 and yDist < .05) else False
		if trial > currentTrial:
			currentTrial = trial
			event_type = "trial_%d_start" % trial
			# adjusting time_since_start to the true start of the trial
			time_since_start -= currentTrialClock
			nid += 1
			w.write("%f\t%d\t%s\n" % (time_since_start, nid, event_type))
			event_type = "trial_%d_avoid_onset" % trial
			time_since_start += 4.0 # length of anticipatory period
			nid += 1
			w.write("%f\t%d\t%s\n" % (time_since_start, nid, event_type))
		elif poppedBalloon == 1:
			event_type = "trial_%d_pop" % trial
			nid += 1
			w.write("%f\t%d\t%s\n" % (time_since_start, nid, event_type))
		elif savedBalloon == 1:
			event_type = "trial_%d_save" % trial
			nid += 1
			w.write("%f\t%d\t%s\n" % (time_since_start, nid, event_type))
		elif should_have_caught:
			event_type = "trial_%d_should_catch" % trial
			nid += 1
			w.write("%f\t%d\t%s\n" % (time_since_start, nid, event_type))

if __name__ == "__main__":
	main()
