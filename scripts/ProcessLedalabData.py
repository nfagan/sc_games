import sys, os, re, argparse
from collections import OrderedDict

source_dir = os.path.abspath(os.path.dirname(__file__))


# This script is adaptable for other experiments except for all the logic relating to early/late avoidance periods
missing_data_symbol = '7777'
event_names = OrderedDict([
	('4','avoidance_onset'),
	('5','aversive_sound'),
	('6','first_contact'),
	('7','target_frozen'),
])

all_conditions = []
for tp in ('T1', 'T2'):
	for name in event_names.values():
		all_conditions.append("%s_%s" % (tp, name))



parser = argparse.ArgumentParser(description="This script produces descriptive statistics by event type for various GSR measures.")
parser.add_argument("-i", "--input", required=True, type=argparse.FileType('r'), help="the GSR text file")
parser.add_argument("-o", "--output", required=True, help="the basename/path to be used for output files (don't include a file extension)")
parser.add_argument("-p", "--participant-id", metavar="ID", required=True, help="the participant id (e.g., 001, 002, 999, etc.)")
parser.add_argument("-t", "--timepoint", metavar="T1|T2", choices=("T1", "T2"), required=True, help="the experiment timepoint (choices: T1, T2)")

args = parser.parse_args()
input_file = args.input
output_base = args.output
participant_id = args.participant_id
timepoint = args.timepoint

output_dir = os.path.dirname(output_base) or os.getcwd() # if no path included, then use working directory
if not os.access(output_dir, os.W_OK):
	print("Error: Output basename/path %s is either invalid or non-writeable.") % output_base
	sys.exit()
else:
	output_base = os.path.abspath(output_base)

spss_file = output_base + '_gsr_stats_spss.txt'

input_headers = input_file.readline().strip()
# put data lines into list after stripping whitespace padding
input_lines = map(lambda line: re.sub(' ', '', line), input_file.read().splitlines())

num_lines = len(input_lines)

# find the indexes of the columns in the input file
input_header_fields = input_headers.split("\t")
nid_col = input_header_fields.index("Event.NID")
cda_nSCR_col = input_header_fields.index("CDA.nSCR")
cda_latency_col = input_header_fields.index("CDA.Latency")
cda_amp_sum_col = input_header_fields.index("CDA.AmpSum")
cda_scr_col = input_header_fields.index("CDA.SCR")
cda_iscr_col = input_header_fields.index("CDA.ISCR")
cda_phasic_max_col = input_header_fields.index("CDA.PhasicMax")
cda_tonic_col = input_header_fields.index("CDA.Tonic")
tpp_nSCR_col = input_header_fields.index("TTP.nSCR")
tpp_latency_col = input_header_fields.index("TTP.Latency")
tpp_amp_sum_col = input_header_fields.index("TTP.AmpSum")
global_mean_col = input_header_fields.index("Global.Mean")
global_max_deflection_col = input_header_fields.index("Global.MaxDeflection")
event_name_col = input_header_fields.index("Event.Name")

# simple nested dictionary implementation
class Tree(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value
data = Tree()

num_avoidance_onsets = 0 # keep track of number of avoidance onsets to ensure the expected number of trials appears
for index, line in enumerate(input_lines):
	# strip space characters, if any
	line = re.sub(' ', '', line)
	fields = line.split("\t")
	event_code = fields[event_name_col]
	event_code = re.sub('"', '', event_code) # strip out quotation marks
	try:
		event_name = event_names[event_code]  # see event_names dict declaration
	except KeyError:
		print("Unexpected event name \"%s\" in input file." % event_code)

	condition = "%s_%s" % (timepoint, event_name)
	if event_name == 'avoidance_onset':
		num_avoidance_onsets += 1

	# Store all data for calculating averages
	## Each value is stored as a tuple: (value, trial_number), where trial number is inferred from number of avoidance onset events

	# first, handle columns that count significant events and their latencies separately
	cda_nSCR = int(fields[cda_nSCR_col])
	tpp_nSCR = int(fields[tpp_nSCR_col])

	cda_nSCR_value = 1 if cda_nSCR >= 1 else 0
	cda_latency_value = float(fields[cda_latency_col]) if cda_nSCR_value == 1 else 0
	data[condition].setdefault(cda_nSCR_col, []).append((cda_nSCR_value, num_avoidance_onsets))
	data[condition].setdefault(cda_latency_col, []).append((cda_latency_value, num_avoidance_onsets))

	tpp_nSCR_value = 1 if tpp_nSCR >= 1 else 0
	tpp_latency_value = float(fields[tpp_latency_col]) if tpp_nSCR_value == 1 else 0

	data[condition].setdefault(tpp_nSCR_col, []).append((tpp_nSCR_value, num_avoidance_onsets))
	data[condition].setdefault(tpp_latency_col, []).append((tpp_latency_value, num_avoidance_onsets))

	# handle rest of columns together
	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col, tpp_amp_sum_col, global_mean_col, global_max_deflection_col):
		data[condition].setdefault(data_col, []).append((float(fields[data_col]), num_avoidance_onsets))

if num_avoidance_onsets != 30:
	print("Error: Expected 30 avoidance period onset events, but found %d." % num_avoidance_onsets)
	print("Since this discrepancy throws off many of this script's calculations, no output file can be created.")
	sys.exit()

# will build up the fields of wide-formatted averages output file while the regular one is being written
wide_header_fields = ["participant_id",]
wide_data_fields = [participant_id,]


# go through data and put together output file
header_fields = ["Condition",]
for header in ("Num_events", "Num_CDA.nSCR", "Avg_CDA.Latency", "Avg_CDA.AmpSum", "Avg_CDA.AmpSum_sqrttrnsfm", 
		"Avg_CDA.SCR", "Avg_CDA.ISCR",  "Avg_CDA.PhasicMax", "Avg_CDA.Tonic", "Num_TTP.nSCR", "Avg_TTP.Latency", 
		"Avg_TTP.AmpSum", "Avg_TTP.AmpSum_sqrttrnsfm", "Avg_Global.Mean", "Avg_Global.MaxDeflection"):
	header_fields.extend([header, header + "_early", header + "_late"])

# going through conditions in a specific order for printing the output file
for condition in all_conditions:
	# add current condition name to list of header fields to create a set of header columns for the wide file
	for header in header_fields[1:]:
		wide_header_fields.append("%s_%s" % (condition, header))

	# calculate averages for all fields (Note that latency averages are calculated across significant events, not all events)
	total_event_count = len(data[condition][cda_nSCR_col])
	first_half_event_count = len(filter(lambda x: x[1] <=15, data[condition][cda_nSCR_col]))
	second_half_event_count = total_event_count - first_half_event_count

	cda_latencies = [x[0] for x in data[condition][cda_latency_col]]
	cda_count = sum(x[0] for x in data[condition][cda_nSCR_col])
	first_half_cda_latencies = [x[0] for x in filter(lambda y: y[1] <= 15, data[condition][cda_latency_col])]
	first_half_cda_count = sum(x[0] for x in filter(lambda y: y[1] <= 15, data[condition][cda_nSCR_col]))
	second_half_cda_latencies = [x[0] for x in filter(lambda y: y[1] > 15, data[condition][cda_latency_col])]
	second_half_cda_count = sum(x[0] for x in filter(lambda y: y[1] > 15, data[condition][cda_nSCR_col]))

	tpp_latencies = [x[0] for x in data[condition][tpp_latency_col]]
	tpp_count = sum([x[0] for x in data[condition][tpp_nSCR_col]])
	first_half_tpp_latencies = [x[0] for x in filter(lambda y: y[1] <= 15, data[condition][tpp_latency_col])]
	first_half_tpp_count = sum(x[0] for x in filter(lambda y: y[1] <= 15, data[condition][tpp_nSCR_col]))
	second_half_tpp_latencies = [x[0] for x in filter(lambda y: y[1] > 15, data[condition][tpp_latency_col])]
	second_half_tpp_count = sum(x[0] for x in filter(lambda y: y[1] > 15, data[condition][tpp_nSCR_col]))


	# start putting together the output
	output_fields = [condition,]
	output_fields.extend([total_event_count, first_half_event_count, second_half_event_count, cda_count, first_half_cda_count, second_half_cda_count])

	# returns an average by summing a list and dividing by a given divisor
	def average(values, divisor):
		return sum(values)/float(divisor) if divisor != 0 else missing_data_symbol

	average_cda_latency = average(cda_latencies, cda_count)
	avg_cda_latency_first_half = average(first_half_cda_latencies, first_half_cda_count)
	avg_cda_latency_second_half = average(second_half_cda_latencies, second_half_cda_count)

	average_tpp_latency = average(tpp_latencies, tpp_count)
	avg_tpp_latency_first_half = average(first_half_tpp_latencies, first_half_tpp_count)
	avg_tpp_latency_second_half = average(second_half_tpp_latencies, second_half_tpp_count)
	output_fields.extend([average_cda_latency, avg_cda_latency_first_half, avg_cda_latency_second_half]) # tpp columns get appended later 

	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col, tpp_nSCR_col, tpp_latency_col, tpp_amp_sum_col, global_mean_col, global_max_deflection_col):
		if data_col is tpp_nSCR_col:
			output_fields.extend([tpp_count, first_half_tpp_count, second_half_tpp_count])
			continue
		elif data_col is tpp_latency_col:
			output_fields.extend([average_tpp_latency, avg_tpp_latency_first_half, avg_tpp_latency_second_half])
			continue
		else:
			all_values = [x[0] for x in data[condition][data_col]]
			first_half_values = [x[0] for x in filter(lambda y: y[1] <= 15, data[condition][data_col])]
			second_half_values = [x[0] for x in filter(lambda y: y[1] > 15, data[condition][data_col])]
			overall_average = average(all_values, total_event_count)
			average_first_half = average(first_half_values, first_half_event_count)
			average_second_half = average(second_half_values, second_half_event_count)
			output_fields.extend([overall_average, average_first_half, average_second_half])

		# add columns with square root transformation for amp_sum data
		if data_col is cda_amp_sum_col or data_col is tpp_amp_sum_col:
			max_value = max(all_values) if data[condition][data_col] else 0
			sqrt_transform = sum(x ** 0.5 for x in all_values) / total_event_count / (max_value ** 0.5) if 0 not in (max_value, total_event_count) else missing_data_symbol
			sqrt_early = sum(x ** 0.5 for x in first_half_values) / first_half_event_count / (max_value ** 0.5) if 0 not in (max_value, first_half_event_count) else missing_data_symbol
			sqrt_late = sum(x ** 0.5 for x in second_half_values) / second_half_event_count / (max_value ** 0.5) if 0 not in (max_value, second_half_event_count) else missing_data_symbol
			output_fields.extend([sqrt_transform, sqrt_early, sqrt_late])

	for datum in output_fields[1:]:
		wide_data_fields.append(datum)
	
# write wide averages output file
spss = open(spss_file, 'w')
spss.write("\t".join(wide_header_fields) + "\n")
spss.write("\t".join([str(x) for x in wide_data_fields]) + "\n")

