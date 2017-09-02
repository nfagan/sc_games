import os, sys, re
from optparse import OptionParser
from datetime import datetime as dt
from datetime import timedelta


# declare, collect and validate user input
parser = OptionParser()
parser.add_option("-i", "--input", metavar="INPUT", dest="input_file", help="The Psychopy task output file (e.g., 085_balloon_cs_Aug-30-17_1552_highlights.txt")
parser.add_option("-o", "--output", metavar="OUTPUT", dest="output_file", help="The name for the event list to be produced by this script")
parser.add_option("-t", "--timestamp", metavar="ACQ_TIMESTAMP", dest="acq_timestamp", help="A timestamp from Acqknowledge, given in quotes (e.g. \"Aug 30 2017 17:05:47\"")
parser.add_option("-l", "--lag", metavar="LAG", dest="timestamp_lag", type="float", help="The number of seconds from start of acquisition until timestamp")
(options, args) = parser.parse_args()
input_file = options.input_file
output_file = options.output_file
raw_acq_timestamp = options.acq_timestamp
lag = options.timestamp_lag

# ensure required arguments are supplied, that files exist, etc.
if not input_file or not output_file or not raw_acq_timestamp or (not lag and lag != 0) or len(args) != 0:
	parser.print_help()
	sys.exit()

if not os.path.isfile(input_file):
	print "Error: The input file \"%s\" does not exist." % input_file
	sys.exit()
else:
	input_file = os.path.abspath(input_file)

if os.path.isfile(output_file):
	print "Error: There is already a file called \"%s\"." % output_file
	sys.exit()

try:
	# convert input timestamp into a datetime object
	raw_acq_timestamp = re.sub("\t", " ", raw_acq_timestamp) # in case a tab character sneaks in due to pasting from Excel
	acq_start = dt.strptime(raw_acq_timestamp, "%b %d %Y %H:%M:%S")
	acq_start = acq_start - timedelta(seconds = lag) # subtracting the offset
	print "Acquisition started at approximately {}".format(acq_start)
except:
	print "Error: Failed to determine acquisition start time from input timestamp/lag values.\n"
	print "Make sure the timestamp is in this format, including quotation marks: \"Apr 09 2017 18:29:01\"\n";
	sys.exit()

try:
	output = open(output_file, 'w')
except:
		print "Error: Could not create output file \"%s\"." %output_file

output.write("time\tnid\tname\n")
nid = 0
with open(input_file, 'r') as f:
	while True:
		line = f.readline()
		if not re.search("^#", line):
			break
	header_fields = line.strip().split("\t")
	num_fields = len(header_fields)
	magic_making_col = header_fields.index("just_made_magic")
	aversive_noise_col = header_fields.index("aversive_noise_onset")
	time_col = header_fields.index("time_of_day_in_seconds")
	trial_col = header_fields.index("trial_num")

	for line in f:
		fields = line.split("\t")
		if len(fields) != num_fields:
			sys.stderr.write("Warning: Some lines in file %s are missing fields.\n" % input_file)
			continue
		gsr_time = float(fields[time_col]) - acq_start.hour * 3600 - acq_start.minute * 60 - acq_start.second - acq_start.microsecond/1000000
		trial_num = int(fields[trial_col])
		if fields[aversive_noise_col] is "1":
			nid += 1
			output.write("%f\t%d\ttrial_%d_aversive_noise\n" % (gsr_time, nid, trial_num))
		if fields[magic_making_col] is "1":
			nid += 1
			output.write("%f\t%d\ttrial_%d_spell_cast\n" % (gsr_time, nid, trial_num))

