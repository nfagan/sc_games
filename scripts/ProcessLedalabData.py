import sys, os, re
from optparse import OptionParser

source_dir = os.path.abspath(os.path.dirname(__file__))

# egg_noise, egg_magic, balloon_noise, balloon_magic

parser = OptionParser()
parser.add_option("-i", "--input", metavar="INPUT", dest="input_file", help="the GSR text file")
parser.add_option("-o", "--output", metavar="OUTPUT", dest="output_base", help="the basename/path to be used for output files (don't include a file extension)")
parser.add_option("-p", "--participant-id", metavar="ID", dest="participant_id", help="the participant id (e.g., 001, 002, 999, etc.)")
parser.add_option("-t", "--timepoint", metavar="T1|T2", dest="timepoint", choices=("T1", "T2"), help="the experiment timepoint (choices: T1, T2)")
(options, args) = parser.parse_args()
input_file = options.input_file
output_base = options.output_base
participant_id = options.participant_id
timepoint = options.timepoint

if len(args) > 0:
	bad_args = ", ".join(args)
	print "Invalid input arguments: %s" % bad_args
	parser.print_help()
	sys.exit()

# validate input arguments
if not input_file or not output_base or not participant_id:
	parser.print_help()
	sys.exit()

if not os.path.isfile(input_file):
	print "Error: Input file %s does not exist." % input_file
	sys.exit()
else:
	input_file = os.path.abspath(input_file)

output_dir = os.path.dirname(output_base) or os.getcwd() # if no path included, then use working directory
if not os.access(output_dir, os.W_OK):
	print "Error: Output basename/path %s is either invalid or non-writeable." % output_base
	sys.exit()
else:
	output_base = os.path.abspath(output_base)

spss_file = output_base + '_gsr_stats_spss.txt'

with open(input_file, 'rU') as f:
	input_headers = f.readline().strip()
	# put data lines into list after stripping whitespace padding
	input_lines = map(lambda line: re.sub(' ', '', line), f.read().splitlines())

num_lines = len(input_lines)
if num_lines > 30:
	print "Warning: More events found (%d) than expected (30)." % (num_lines)
	print "Some calculations may be off."
elif num_lines < 30:
	print "Warning: Fewer events found (%d) than expected (30)." % (num_lines)
	print "Some calculations (e.g., early/late trial averages) may be off."

Num_events = num_lines

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

for index, line in enumerate(input_lines):
	# strip space characters, if any
	line = re.sub(' ', '', line)
	fields = line.split("\t")
	event_name = fields[event_name_col]
	if re.search("aversive_noise", event_name):
		event_type = "aversive_noise"
	elif re.search("save", event_name):
		event_type = "save"
	else:
		print "Error: The input file had an event that couldn't be categorized as \"aversive_noise\" or \"save.\""
		sys.exit()

	condition = "%s_%s" % (timepoint, event_type)

	## Store all data for calculating averages

	# first, handle columns that count significant events and their latencies separately
	cda_nSCR = int(fields[cda_nSCR_col])
	tpp_nSCR = int(fields[tpp_nSCR_col])
	if condition not in data:
		data[condition][cda_latency_col] = []
		data[condition][cda_nSCR_col] = []
		data[condition][tpp_latency_col] = []
		data[condition][tpp_nSCR_col] = []

	if cda_nSCR >= 1:
		data[condition][cda_nSCR_col].append(1)
		data[condition][cda_latency_col].append(float(fields[cda_latency_col]))
	else:
		data[condition][cda_nSCR_col].append(0)
		data[condition][cda_latency_col].append(0)
	if tpp_nSCR >= 1:
		data[condition][tpp_nSCR_col].append(1)
		data[condition][tpp_latency_col].append(float(fields[tpp_latency_col]))
	else:
		data[condition][tpp_nSCR_col].append(0)
		data[condition][tpp_latency_col].append(0)

	# handle rest of columns together
	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col, tpp_amp_sum_col, global_mean_col, global_max_deflection_col):
		if not data[condition][data_col]:
			data[condition][data_col] = []
		data[condition][data_col].append(float(fields[data_col]))



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
for condition in ("%s_aversive_noise" % timepoint, "%s_save" % timepoint):
	# add current condition name to list of header fields to create a set of header columns for the wide file
	for header in header_fields[1:]:
		wide_header_fields.append("%s_%s" % (condition, header))
	# calculate averages for all fields (Note that latency averages are calculated across significant events, not all events)
	event_count = len(data[condition][cda_nSCR_col])
	midpoint = event_count / 2
	if event_count % 2 != 0:
		print "Warning: Odd number of events found condition %s." % condition
		print "Some fields (e.g., first and second half averages) may be calculated incorrectly."
	cda_count = sum(data[condition][cda_nSCR_col])
	first_half_cda = sum(data[condition][cda_nSCR_col][0:midpoint]) if data[condition][cda_nSCR_col] else 0
	second_half_cda = cda_count - first_half_cda
	tpp_count = sum(data[condition][tpp_nSCR_col])
	first_half_tpp = sum(data[condition][tpp_nSCR_col][0:midpoint]) if data[condition][tpp_nSCR_col] else 0
	second_half_tpp = tpp_count - first_half_tpp
	output_fields = [condition,]
	output_fields.extend(str(field) for field in (event_count, midpoint, midpoint, cda_count, first_half_cda, second_half_cda))

	average_cda_latency = sum(data[condition][cda_latency_col]) / float(cda_count) if cda_count != 0 else "NA"
	avg_cda_latency_first_half = sum(data[condition][cda_latency_col][0:midpoint]) / float(first_half_cda) if first_half_cda != 0 else "NA"
	avg_cda_latency_second_half = sum(data[condition][cda_latency_col][midpoint:event_count]) / float(second_half_cda) if second_half_cda != 0 else "NA"
	average_tpp_latency = sum(data[condition][tpp_latency_col]) / float(tpp_count) if tpp_count != 0 else "NA"
	avg_tpp_latency_first_half = sum(data[condition][tpp_latency_col][0:midpoint]) / float(first_half_tpp) if first_half_tpp != 0 else "NA"
	avg_tpp_latency_second_half = sum(data[condition][tpp_latency_col][midpoint:event_count]) / float(second_half_tpp) if second_half_tpp != 0 else "NA"
	output_fields.extend(str(field) for field in [average_cda_latency, avg_cda_latency_first_half, avg_cda_latency_second_half]) # tpp columns get appended later 

	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col, tpp_nSCR_col, tpp_latency_col, tpp_amp_sum_col, global_mean_col, global_max_deflection_col):
		if data_col is tpp_nSCR_col:
			output_fields.extend(str(field) for field in (tpp_count, first_half_tpp, second_half_tpp))
			continue
		elif data_col is tpp_latency_col:
			output_fields.extend(str(field) for field in (average_tpp_latency, avg_tpp_latency_first_half, avg_tpp_latency_second_half))
			continue
		else:
			average_value = sum(data[condition][data_col]) / event_count if event_count != 0 else "NA"
			average_first_half = sum(data[condition][data_col][0:midpoint]) / midpoint if event_count != 0 else "NA"
			average_second_half = sum(data[condition][data_col][midpoint:event_count]) / midpoint if event_count != 0 else "NA"
			output_fields.extend(str(field) for field in (average_value, average_first_half, average_second_half))

		# add columns with square root transformation for amp_sum data, using training data for the max values
		if data_col is cda_amp_sum_col or data_col is tpp_amp_sum_col:
			max_value = max(data[condition][data_col]) if data[condition][data_col] else 0
			sqrt_transform = sum(x ** 0.5 for x in data[condition][data_col]) / event_count / (max_value ** 0.5) if 0 not in (max_value, event_count) else "NA"
			sqrt_early = sum(x ** 0.5 for x in data[condition][data_col][0:midpoint]) / midpoint / (max_value ** 0.5) if 0 not in (max_value, midpoint) else "NA"
			sqrt_late = sum(x ** 0.5 for x in data[condition][data_col][midpoint:event_count]) / midpoint / (max_value ** 0.5) if 0 not in (max_value, midpoint) else "NA"
			output_fields.extend(str(field) for field in (sqrt_transform, sqrt_early, sqrt_late))

	for datum in output_fields[1:]:
		wide_data_fields.append(datum)
	
# write wide averages output file
spss = open(spss_file, 'w')
spss.write("\t".join(wide_header_fields) + "\n")
spss.write("\t".join(wide_data_fields) + "\n")

