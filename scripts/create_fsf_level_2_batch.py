#!/usr/bin/env python
import sys, os, argparse, re

# this directory will hold level 2 output for all subjects
level_2_dir = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/pre_diss_3_18/level_2/'

# project-specific template file
template = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/reference/sc-level-2-template_sc2.fsf'

parser = argparse.ArgumentParser(description='Creates an sbatch script to run level 2 analyses for a subject')
parser.add_argument('-s', '--subject-id', metavar='ID', required=True, help="the subject ID")
parser.add_argument('-f1', required=True, help="sc2 part 1 feat directory")
parser.add_argument('-f2', required=True, help="sc2 part 2 feat directory")

args = parser.parse_args()

legal_id = "^\d\d\d$"
if not re.search(legal_id, args.subject_id):
	print("Bad subject ID. Should be three digits.")
	sys.exit()

for directory in (args.f1, args.f2):
	if not os.path.isdir(directory):
		print("Error: Directory %s not found." % directory)
		sys.exit()

subject_directory = level_2_dir + args.subject_id
feat_output_directory = subject_directory + '/sc2_level_2_' + args.subject_id

try:
	os.rmdir(subject_directory)
except OSError:
	pass
os.mkdir(subject_directory)

with open(template, 'r') as f:
	template_text = f.read()

# plug subject-specific variables into template text
template_text = re.sub('OUTPUT_DIRECTORY', feat_output_directory, template_text)
template_text = re.sub('FEAT_DIRECTORY_1', os.path.abspath(args.f1), template_text)
template_text = re.sub('FEAT_DIRECTORY_2', os.path.abspath(args.f2), template_text)

# define and write design file
design_file = subject_directory + "/design_%s.fsf" % args.subject_id
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
#SBATCH --workdir=%(subject_directory)s
#SBARCH --job-name=feat_%(subject_id)s
#SBATCH --output=%(subject_directory)s/slurm.feat_%(subject_id)s.%%j.log
#SBATCH --error=%(subject_directory)s/slurm.feat_%(subject_id)s.%%j.log
module load Apps/FSL/5.0.10
 . /nexsan/apps/hpc/Apps/FSL/5.0.10/etc/fslconf/fsl.sh

feat %(design_file)s
''' % {'design_file': design_file, 'subject_directory': subject_directory, 'subject_id': args.subject_id}

# format and save script
script = re.sub('^\n', '', script)
script_name = subject_directory + '/run_level_2_sub_' + args.subject_id + '.sh'
with open(script_name, 'w') as f:
	f.write(script)

print("An sbatch-ready script has been created here: %s" % script_name)




