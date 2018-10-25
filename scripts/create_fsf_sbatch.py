#!/usr/bin/env python
import sys, os, argparse, re

# project-specific output directory
feat_output_directory = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/isdp_analyses_2018/level_1/'

# project-specific template file
template = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/reference/sc-level-1-template.fsf'

parser = argparse.ArgumentParser(description='Creates an sbatch script to run level 1 analyses for a subject')
parser.add_argument('-s', '--subject-id', metavar='ID', required=True, help="the subject ID")
parser.add_argument('-f1', required=True, help="sc2 part 1 image file basename")
parser.add_argument('-f2', required=True, help="sc2 part 2 image file basename")
parser.add_argument('-intersect', '--intersection-timing', required=True, help="intersection timing file")
parser.add_argument('-antic', '--anticipatory-timing', required=True, help="anticipatory period timing file")
parser.add_argument('-avoid', '--avoidance-timing', required=True, help="avoidance period timing file")
parser.add_argument('-aversive', '--aversive-timing', required=True, help="aversive noise timing file")
parser.add_argument('-m','--motion', dest='motion_file', required=True, help="motion regressors text file")

args = parser.parse_args()

legal_id = "^\d\d\d$"
if not re.search(legal_id, args.subject_id):
	print("Bad subject ID. Should be three digits.")
	sys.exit()

for basename in (args.f1, args.f2):
	if not os.path.isfile(basename + '.nii.gz'):
		print("Error: could not find files associated with basename \"%s\"." % basename)
for file in (args.intersection_timing, args.anticipatory_timing, args.avoidance_timing, args.aversive_timing, args.motion_file):
	if not os.path.isfile(file):
		print("Error: file \"%s\" does not exist." % file)
		sys.exit()

output_directory = feat_output_directory + args.subject_id + '/'

try:
	os.rmdir(output_directory)
except OSError:
	pass
os.mkdir(output_directory)

with open(template, 'r') as f:
	template_text = f.read()

# plug subject-specific variables into template text
template_text = re.sub('OUTPUT_DIRECTORY', output_directory, template_text)
template_text = re.sub('FEAT_FILE_1', os.path.abspath(args.f1), template_text)
template_text = re.sub('FEAT_FILE_2', os.path.abspath(args.f2), template_text)
template_text = re.sub('EV_FILE_1', os.path.abspath(args.intersection_timing), template_text)
template_text = re.sub('EV_FILE_2', os.path.abspath(args.anticipatory_timing), template_text)
template_text = re.sub('EV_FILE_3', os.path.abspath(args.avoidance_timing), template_text)
template_text = re.sub('EV_FILE_4', os.path.abspath(args.aversive_timing), template_text)
template_text = re.sub('MOTION_FILE', os.path.abspath(args.motion), template_text)

# define and write design file
design_file = output_directory + "design_%s.fsf" % args.subject_id
with open(design_file, 'w') as f:
	f.write(template_text)

# create an sbatch script
script = '''
#!/bin/bash
#SBATCH --partition=long
#SBATCH --nodes=1
#SBATCH --mem-per-cpu=30G
#SBATCH --time=15:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=emily.cohodes@yale.edu
#SBATCH --workdir=%(output_directory)s
#SBARCH --job-name=feat_%(subject_id)s
#SBATCH --output=%(output_directory)sslurm.%%J.%%j.log
#SBATCH --error=%(output_directory)sslurm.%%J.%%j.log
module load Apps/FSL/5.0.10
 . /nexsan/apps/hpc/Apps/FSL/5.0.10/etc/fslconf/fsl.sh

feat %(design_file)s
''' % {'design_file': design_file, 'output_directory': output_directory, 'subject_id': args.subject_id}

# format and save script
script = re.sub('^\n', '', script)
script_name = output_directory + 'run_level_1_sub_' + args.subject_id + '.sh'
with open(script_name, 'w') as f:
	f.write(script)

print("An sbatch-ready script has been created here: %s" % script_name)


