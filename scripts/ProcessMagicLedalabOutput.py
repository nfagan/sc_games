import sys, os, re
from optparse import OptionParser

source_dir = os.path.abspath(os.path.dirname(__file__))

# egg_noise, egg_magic, balloon_noise, balloon_magic

parser = OptionParser()
parser.add_option("-i", "--input", metavar="INPUT", dest="input_file", help="the GSR text file")
parser.add_option("-o", "--output", metavar="OUTPUT", dest="output_base", help="the basename/path to be used for output files (don't include an extension)")
parser.add_option("-p", "--participant-id", metavar="ID", dest="participant_id", help="the participant id (e.g., 001, 002, 999, etc.)")
parser.add_option("-t", "--timepoint", metavar="T1|T2", dest="timepoint", choices=("T1", "T2"), help="the relevant game type (choices: T1, T2)")
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
if not input_file or not output_base:
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
	input_lines = f.read().splitlines()


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

totals_by_condition = {}
count_by_condition = {}

# simple nested dictionary implementation
class Tree(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

cda_count_by_condition = {}
cda_totals_by_condition = Tree()
cda_totals_all = Tree()

tpp_count_by_condition = {}
tpp_totals_by_condition = Tree()
tpp_totals_all = Tree()

condition_counts = {}
global_mean_total_by_condition = {}
max_deflection_total_by_condition = {}

for index, line in enumerate(input_lines):
	# strip space characters, if any
	line = re.sub(' ', '', line)
	fields = line.split("\t")
	event_name = fields[event_name_col]
	if re.search("aversive_noise", event_name):
		event_type = "aversive_noise"
	elif re.search("spell_cast", event_name):
		event_type = "spell_cast"
	else:
		print "Error: The input file had an event that couldn't be categorized as \"spell_cast\" or \"aversive_noise.\""
		sys.exit()

	condition = "%s_%s" % (timepoint, event_type)
	global_mean = float(fields[global_mean_col])
	global_max_deflection = float(fields[global_max_deflection_col])
	if condition in condition_counts:
		condition_counts[condition] += 1
		global_mean_total_by_condition[condition] += global_mean
		max_deflection_total_by_condition[condition] += global_max_deflection
	else:
		condition_counts[condition] = 1
		global_mean_total_by_condition[condition] = global_mean
		max_deflection_total_by_condition[condition] = global_max_deflection

	# work towards average calculations
	cda_nSCR = int(fields[cda_nSCR_col])
	if cda_nSCR >= 1:
		if condition in cda_count_by_condition:
			cda_count_by_condition[condition] += 1
		else:
			cda_count_by_condition[condition] = 1
		for data_col in (cda_latency_col, cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col):
			if not cda_totals_by_condition[condition][data_col]:
				cda_totals_by_condition[condition][data_col] = float(fields[data_col])
			else:
				cda_totals_by_condition[condition][data_col] += float(fields[data_col])
	
	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col):
		if not cda_totals_all[condition][data_col]:
			cda_totals_all[condition][data_col] = float(fields[data_col])
		else:
			cda_totals_all[condition][data_col] += float(fields[data_col])


	tpp_nSCR = int(fields[tpp_nSCR_col])
	if tpp_nSCR >= 1:
		if condition in tpp_count_by_condition:
			tpp_count_by_condition[condition] += 1
		else:
			tpp_count_by_condition[condition] = 1
		for data_col in (tpp_latency_col, tpp_amp_sum_col):
			if not tpp_totals_by_condition[condition][data_col]:
				tpp_totals_by_condition[condition][data_col] = float(fields[data_col])
			else:
				tpp_totals_by_condition[condition][data_col] += float(fields[data_col])
	
	if not tpp_totals_all[condition][tpp_amp_sum_col]:
		tpp_totals_all[condition][tpp_amp_sum_col] = float(fields[tpp_amp_sum_col])
	else:
		tpp_totals_all[condition][tpp_amp_sum_col] += float(fields[tpp_amp_sum_col])


# will build up the fields of wide-formatted averages output file while the regular one is being written
wide_header_fields = ["participant_id",]
wide_data_fields = [participant_id,]


# go through data and put together output file
header_fields = ("Sample", "Num_events", "Num_CDA.nSCR", "Avg_CDA.Latency_thresh", "Avg_CDA.AmpSum_thresh", "Avg_CDA.SCR_thresh", "Avg_CDA.ISCR_thresh",  
	"Avg_CDA.PhasicMax_thresh", "Avg_CDA.Tonic_thresh", "Avg_CDA.AmpSum_nonthresh", "Avg_CDA.SCR_nonthresh", "Avg_CDA.ISCR_nonthresh", 
	"Avg_CDA.PhasicMax_nonthresh", "Avg_CDA.Tonic_nonthresh", "Num_TTP.nSCR", "Avg_TTP.Latency_thresh", "Avg_TTP.AmpSum_thresh", 
	"Avg_TTP.AmpSum_nonthresh", "Avg_Global.Mean", "Avg_Global.MaxDeflection")

# going through conditions in a specific order for printing the output file
for condition in ("%s_aversive_noise" % timepoint, "%s_spell_cast" % timepoint):
	# add current condition name to list of header fields to create a set of header columns for the wide file
	for header in header_fields[1:]:
		wide_header_fields.append("%s_%s" % (condition, header))

	# calculate averages
	event_count = condition_counts.get(condition, 0)
	cda_count = cda_count_by_condition.get(condition, 0)
	condition_output_fields = [str(event_count), str(cda_count)]

	# averages for above-threshold events
	for data_col in (cda_latency_col, cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col):
		average_value = cda_totals_by_condition[condition][data_col] / cda_count if cda_count != 0 else "NA"
		condition_output_fields.append(str(average_value))

	# averages across all trials (regardless of threshold)
	for data_col in (cda_amp_sum_col, cda_scr_col, cda_iscr_col, cda_phasic_max_col, cda_tonic_col):
		average_value = cda_totals_all[condition][data_col] / event_count if event_count != 0 else "NA"
		condition_output_fields.append(str(average_value))

	# repeat for tpp fields
	tpp_count = tpp_count_by_condition.get(condition, 0)
	condition_output_fields.append(str(tpp_count))
	for data_col in (tpp_latency_col, tpp_amp_sum_col):
		average_value = tpp_totals_by_condition[condition][data_col] / tpp_count if tpp_count != 0 else "NA"
		condition_output_fields.append(str(average_value))
	for data_col in (tpp_amp_sum_col,):
		average_value = tpp_totals_all[condition][data_col] / event_count if event_count != 0 else "NA"
		condition_output_fields.append(str(average_value))

	avg_global_mean = global_mean_total_by_condition.get(condition, 0) / event_count if global_mean_total_by_condition.get(condition, 0) != 0 else "NA"
	avg_max_deflection = max_deflection_total_by_condition.get(condition, 0) / event_count if max_deflection_total_by_condition.get(condition, 0) != 0 else "NA"

	# combine results, print to averages file, and append values to wide output file's data fields
	condition_output_fields.extend([str(avg_global_mean), str(avg_max_deflection)])
	for datum in condition_output_fields:
		wide_data_fields.append(datum)
	
# write wide averages output file
spss = open(spss_file, 'w')
spss.write("\t".join(wide_header_fields) + "\n")
spss.write("\t".join(wide_data_fields) + "\n")

