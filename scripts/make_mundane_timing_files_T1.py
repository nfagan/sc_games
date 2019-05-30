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

# define output file prefixes (more gets added later)
aversive_timing_file = output_dir + '/aversive_noise_timing'
antic_timing_file = output_dir + '/antic_period_timing'
avoid_timing_file = output_dir + '/avoid_period_timing'
intersection_timing_file = output_dir + '/intersection_timing'

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


## Find MRI start times for first and second scans (basing second start time on long break)
#adjusting for subtraction of 8 volumes from beginning of scan due to conversation with PO 3/20/18 (8 TRs x .8 seconds per TR)
first_mri_start_time = float(mri.readline().strip().split("\t")[-1])
previous_time = first_mri_start_time
first_mri_start_time += 6.4
second_mri_start_time = None

for line in mri:
	fields = line.strip().split("\t")
	trigger_num = int(fields[0])
	timepoint = float(fields[1])
	# a long break in TRs indicates start of new scan
	if timepoint - previous_time > 60:
		second_mri_start_time = timepoint
		if trigger_num != 374: # expected start of second scan 
			print("Warning: Second scan was expected to start with trigger number 374, but it seems to have started at trigger %d." % trigger_num)
		break
	previous_time = timepoint
if not second_mri_start_time:
	print("Error: Could not deduce start time of the second MRI scan from the trigger file.")
	sys.exit()
second_mri_start_time += 6.4
mri_start_times = (first_mri_start_time, second_mri_start_time)


# make output directory
try:
	os.mkdir(output_dir)
except OSError:
	print("Error: Couldn't create the specified output directory.")
	sys.exit()


# skip to header line of data file and find relevant columns
for line in f:
	if re.search('^#', line):
		continue
	header_fields = line.split("\t")
	aversive_noise_onset_col = header_fields.index('aversive_noise_onset')
	antic_period_onset_col = header_fields.index('antic_period_onset')
	avoid_period_onset_col = header_fields.index('avoid_period_onset')
	intersection_col = header_fields.index('touching_target_object')
	time_col = header_fields.index('time_of_day_in_seconds')
	trial_col = header_fields.index('trial_num')
	break

# track events (one list for first half of trials, one list for second half of trials)
aversive_noise_events = [[], []]
antic_period_events = [[], []]
avoid_period_events = [[], []]
intersection_events = [[], []]

def convert_time(t, part):
	return str(float(t) - mri_start_times[part])

# process data
current_intersection_start_time = None

for line in f:
	fields = line.split("\t")
	trial_num = int(fields[trial_col])
	part = 0 if trial_num < 16 else 1 # 0 = first half, 1 = second half
	time_in_task = convert_time(fields[time_col], part)
	if fields[aversive_noise_onset_col] == '1':
		aversive_noise_events[part].append((time_in_task, '.5')) # duration = .5 for noise
	if fields[antic_period_onset_col] == '1':
		antic_period_events[part].append((time_in_task, '4.0')) # duration = 4.0 for anticipatory period
	if fields[avoid_period_onset_col] == '1':
		avoid_period_events[part].append((time_in_task, '4.5')) # duration = 4.5 for avoidance period
	if fields[intersection_col] == '1':
		if current_intersection_start_time:
			continue
		else:
			current_intersection_start_time = float(time_in_task)
	elif current_intersection_start_time:
		intersection_duration = str(float(time_in_task) - current_intersection_start_time) # approximately, at least
		intersection_events[part].append((current_intersection_start_time, intersection_duration))
		current_intersection_start_time = None
	f_pos = f.tell()


for events, file in ((aversive_noise_events, aversive_timing_file), (antic_period_events, antic_timing_file),
  (avoid_period_events, avoid_timing_file), (intersection_events, intersection_timing_file)):
	for part in (0, 1):
		output_file = file + '_sc1p' + str(part + 1) + "_%s.txt" % subject
		with open(output_file, 'w') as w:
			for time, duration in events[part]:
				w.write("%s\t%s\t1\n" %(time, duration)) # FSL wants a 1 in every row
	



