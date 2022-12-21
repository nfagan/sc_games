import sys, os, re, argparse


timing_file_time_offset = 6.4 # 6.4 seconds (i.e., 8 trs) must added to timing file timestamps to synchronize with motion stats

description = '''
	This script takes in a FSL motion stats file (text format) and a list of timing files (one per experiment part/sample).
	For each part/sample, it calculates and reports average motion across all events in the timing file.
'''

timing_file_help = '''
	A tab-delimited list of timing files, with the following columns: sample name, 
	experiment run name  (e.g. SC1_1, SC2_2, rest), and file path.
'''
motion_file_help = 'A motion stats file in text format with information for all samples/parts in the input list'
parser = argparse.ArgumentParser(description=description)
parser.add_argument("--timing-file-list", required=True, type=argparse.FileType('r'), help=timing_file_help)
parser.add_argument("--motion-file", required=True, type=argparse.FileType('r'), help=motion_file_help)
args = parser.parse_args()

all_timing_files = set()
sample_run_tuples = set()

# read in list of timing files
for num, line in enumerate(args.timing_file_list, start = 1):
	line = line.strip()
	if re.search('^[ \s]*$', line):
		continue
	fields = line.split("\t")
	if len(fields) != 3:
		print("Error: Incorrect formatting in line %d of timing file list." % num)
		sys.exit()
	(sample_name, run_name, file) = fields[0:3]
	if not os.path.isfile(file):
		print("Error: Timing file \"%f\" (line %d of input list) cannot be found." %(file, num))
		sys.exit()

	if file in all_timing_files:
		print("Error: File \"%f\" appears multiple times in input file list." % file)
		sys.exit()

	all_timing_files.add(file)

	if (sample_name, run_name) in sample_run_tuples:
		print("Error: The sample/run combination \"%f\", \"%f\" appears multiple times in input file list." % (sample_name, run_name))
	sample_run_tuples.add((sample_name, run_name))

subject_line = args.motion_file.readline().strip()
subjects_with_motion_data = subject_line.split("\t")[1:]
print(subects_with_motion_data)



