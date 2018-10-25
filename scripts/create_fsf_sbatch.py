#!/usr/bin/env python
import sys, os, argparse, re

# project-specific output directory
level_1_directory = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/pre_diss_3_18/level_1/'

# project-specific template file
template = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/reference/sc-level-1-template_sc2p1_sc2p2.fsf'

parser = argparse.ArgumentParser(description='Creates an sbatch script to run level 1 analyses for a subject')
parser.add_argument('-s', '--subject-id', metavar='ID', required=True, help="the subject ID")
parser.add_argument('-f', required=True, help="sc2 image file basename")
parser.add_argument('-intersect', '--intersection-timing', required=True, help="intersection timing file")
parser.add_argument('-antic', '--anticipatory-timing', required=True, help="anticipatory period timing file")
parser.add_argument('-avoid', '--avoidance-timing', required=True, help="avoidance period timing file")
parser.add_argument('-aversive', '--aversive-timing', required=True, help="aversive noise timing file")
parser.add_argument('-p', '--part', required=True, type=int, choices=(1, 2), help="sc2 part 1 or 2")

args = parser.parse_args()

legal_id = "^\d\d\d$"
if not re.search(legal_id, args.subject_id):
	print("Bad subject ID. Should be three digits.")
	sys.exit()

if not os.path.isfile(args.f + '.nii.gz'):
	print("Error: could not find files associated with basename \"%s\"." % args.f)

for file in (args.intersection_timing, args.anticipatory_timing, args.avoidance_timing, args.aversive_timing):
	if not os.path.isfile(file):
		print("Error: file \"%s\" does not exist." % file)
		sys.exit()

part = str(args.part)
level_1_directory += "sc2p%s/" % part
subject_directory = level_1_directory + args.subject_id
feat_output_directory = subject_directory + "/sc2p%s_level_1_%s" % (part, args.subject_id)

try:
	os.rmdir(subject_directory)
except OSError:
	pass
os.mkdir(subject_directory)

with open(template, 'r') as f:
	template_text = f.read()

# plug subject-specific variables into template text
template_text = re.sub('OUTPUT_DIRECTORY', feat_output_directory, template_text)
template_text = re.sub('FEAT_DIRECTORY', os.path.abspath(args.f), template_text)
template_text = re.sub('EV_FILE_1', os.path.abspath(args.intersection_timing), template_text)
template_text = re.sub('EV_FILE_2', os.path.abspath(args.anticipatory_timing), template_text)
template_text = re.sub('EV_FILE_3', os.path.abspath(args.avoidance_timing), template_text)
template_text = re.sub('EV_FILE_4', os.path.abspath(args.aversive_timing), template_text)

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
script_name = subject_directory + "/run_level_1_p%s_" % part + 'sub_' + args.subject_id + '.sh'
with open(script_name, 'w') as f:
	f.write(script)

print("An sbatch-ready script has been created here: %s" % script_name)




