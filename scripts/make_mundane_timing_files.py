#!/usr/bin/env python
import sys, os, re, argparse

parser = argparse.ArgumentParser(description='Reads in output file ("highlights" are fine) from mundane sc experiment and produces timing files for FSL level 1 analyses.')
parser.add_argument('-i', '--input', required=True, type=argparse.FileType('r'), help="the highlights (or full) output file from the experiment")
parser.add_argument('-m', '--mri-trigger-log', dest='mri', required=True, type=argparse.FileType('r'), help="the log file listing MRI trigger timestamps")
parser.add_argument('-s', '--subject-id', metavar='ID', required=True, help="the subject ID")
parser.add_argument('-o', '--output', required=True, help="the name/path of a new directory to store the timing files")
args = parser.parse_args()

f = args.input
output_dir = args.output
output_dir = re.sub('\/+$', '', output_dir) # strip trailing slashes, if any
mri = args.mri # file handle for mri trigger file
subject = args.subject_id

# define output files
aversive_timing_file = output_dir + '/aversive_noise_timing_%s.txt' % subject
antic_timing_file = output_dir + '/antic_period_timing_%s.txt' % subject
avoid_timing_file = output_dir + '/avoid_period_timing_%s.txt' % subject
intersection_timing_file = output_dir + '/intersection_timing_%s.txt' % subject

# make sure subject ID makes sense
if len(subject) != 3:
	print("Error: Subject ID should be 3 characters.")
	sys.exit()

# make sure output directory is valid, and then create it
try:
	os.rmdir(output_dir)
except OSError:
	pass

if os.path.isdir(output_dir):
	print("Error: Output directory already exists.")
	sys.exit()

mri_start_time = float(mri.readline().strip().split("\t")[-1])

try:
	os.mkdir(output_dir)
except OSError:
	print("Error: Couldn't create the specified output directory.")
	sys.exit()


# skip to header line and find relevant columns
for line in f:
	if re.search('^#', line):
		continue
	header_fields = line.split("\t")
	aversive_noise_onset_col = header_fields.index('aversive_noise_onset')
	antic_period_onset_col = header_fields.index('antic_period_onset')
	avoid_period_onset_col = header_fields.index('avoid_period_onset')
	intersection_col = header_fields.index('touching_target_object')
	time_col = header_fields.index('time_of_day_in_seconds')
	break

# track events
aversive_noise_events = []
antic_period_events = []
avoid_period_events = []
intersection_events = []

def convert_time(t):
	return str(float(t) - mri_start_time)

# process data
current_intersection_start_time = None

for line in f:
	fields = line.split("\t")
	time_in_task = convert_time(fields[time_col])
	if fields[aversive_noise_onset_col] == '1':
		aversive_noise_events.append((time_in_task, '.5')) # duration = .5 for noise
	if fields[antic_period_onset_col] == '1':
		antic_period_events.append((time_in_task, '4.0')) # duration = 4.0 for anticipatory period
	if fields[avoid_period_onset_col] == '1':
		avoid_period_events.append((time_in_task, '4.5')) # duration = 4.5 for avoidance period
	if fields[intersection_col] == '1':
		if current_intersection_start_time:
			continue
		else:
			current_intersection_start_time = float(time_in_task)
	elif current_intersection_start_time:
		intersection_duration = str(float(time_in_task) - current_intersection_start_time) # approximately, at least
		intersection_events.append((current_intersection_start_time, intersection_duration))
		current_intersection_start_time = None

for events, file in ((aversive_noise_events, aversive_timing_file), (antic_period_events, antic_timing_file),
  (avoid_period_events, avoid_timing_file), (intersection_events, intersection_timing_file)):
	with open(file, 'w') as w:
		for time, duration in events:
			w.write("%s\t%s\t1\n" %(time, duration)) # FSL wants a 1 in every row
	



