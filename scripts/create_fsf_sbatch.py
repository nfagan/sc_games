#!/usr/bin/env python
import sys, os, argparse, re


## This script is for making 2 FEAT files, one each for SC2p1 and SC2p2

# project FSF template file
template = '/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/reference/sc-level-1-template.fsf'

parser = argparse.ArgumentParser(description='Creates sc2p1 and sc2p2 sbatch scripts for level 1 analyses of a subject')
parser.add_argument('-s', '--subject-id', metavar='ID', required=True, help="the subject ID")
args = parser.parse_args()

subject_id = args.subject_id
legal_id = "^\d\d\d$"
if not re.search(legal_id, subject_id):
	print("Bad subject ID. Should be three digits.")
	sys.exit()


### data file paths, with subject IDs inserted
### these files should all have been generated in previous processing steps

# project directories on Milgram
analyses = "/gpfs/milgram/project/gee_dylan/candlab/analyses/sc/isdp_analyses_2018"
data = "/gpfs/milgram/project/gee_dylan/candlab/data/mri/hcp_pipeline_preproc/scer"

# basenames feat files for parts 1 and 2
f1 = "%s/sub-A%s/MNINonLinear/Results/ses-scerV1_task-sc2part1_bold/ses-scerV1_task-sc2part1_bold_8dv" % (data, subject_id)
f2 = "%s/sub-A%s/MNINonLinear/Results/ses-scerV1_task-sc2part2_bold/ses-scerV1_task-sc2part2_bold_8dv" % (data, subject_id)
feat_files = (f1, f2)

# timing files for parts 1 and 2
intersect_p1 = "%s/timing_files/%s/intersection_timing_sc2p1_%s.txt" % (analyses, subject_id, subject_id)
intersect_p2 = "%s/timing_files/%s/intersection_timing_sc2p2_%s.txt" % (analyses, subject_id, subject_id)
intersect = (intersect_p1, intersect_p2)

antic_p1 = "%s/timing_files/%s/antic_period_timing_sc2p1_%s.txt" % (analyses, subject_id, subject_id)
antic_p2 = "%s/timing_files/%s/antic_period_timing_sc2p2_%s.txt" % (analyses, subject_id, subject_id)
antic = (antic_p1, antic_p2)

avoid_p1 = "%s/timing_files/%s/avoid_period_timing_sc2p1_%s.txt" % (analyses, subject_id, subject_id)
avoid_p2 = "%s/timing_files/%s/avoid_period_timing_sc2p2_%s.txt" % (analyses, subject_id, subject_id)
avoid = (avoid_p1, avoid_p2)

aversive_p1 = "%s/timing_files/%s/aversive_noise_timing_sc2p1_%s.txt" % (analyses, subject_id, subject_id)
aversive_p2 = "%s/timing_files/%s/aversive_noise_timing_sc2p2_%s.txt" % (analyses, subject_id, subject_id)
aversive = (aversive_p1, aversive_p2)

motion_p1 = "%s/sub-A%s/MNINonLinear/Results/ses-scerV1_task-sc2part1_bold/Movement_Regressors_8dv.txt" % (data, subject_id)
motion_p2 = "%s/sub-A%s/MNINonLinear/Results/ses-scerV1_task-sc2part2_bold/Movement_Regressors_8dv.txt" % (data, subject_id)
motion = (motion_p1, motion_p2)

# Level 1 FSL directories
level1_p1 = "%s/level_1/sc2p1" % analyses
level1_p2 = "%s/level_1/sc2p2" % analyses


# Make sure all expected files exist
missing_files = []
for basename in (f1, f2):
	if not os.path.isfile(basename + '.nii.gz'):
		missing_files.append(basename + '.nii.gz')
for group in (intersect, antic, avoid, aversive, motion):
	for file in group:
		if not os.path.isfile(file):
			missing_files.append(file)

# If files are missing, list them and quit
if len(missing_files) > 0:
	print("Error: The following files could not be found:")
	for file in missing_files:
		print("\t%s" % file)
	print("\nMake sure that theses files exist and that you have entered their paths correctly.")
	sys.exit()

# Creat sc2p1/sc2p2 subject-level output directories
subject_output_p1 = "%s/%s" % (level1_p1, subject_id)
subject_output_p2 = "%s/%s" % (level1_p2, subject_id)
subject_output = (subject_output_p1, subject_output_p2)

# Define feat output directories (get created by FSL, with a .feat extension)
feat_output_p1 = "%s/%s_sc2p1" % (subject_output[0], subject_id)
feat_output_p2 = "%s/%s_sc2p2" % (subject_output[1], subject_id)
feat_output = (feat_output_p1, feat_output_p2)

# Try to create subject-level output directories
for directory in subject_output:
	try:
		os.rmdir(directory)
	except OSError:
		pass
	os.mkdir(directory)

with open(template, 'r') as f:
	template_text = f.read()

script_names = [] # to save names of sbatch scripts
for i in (0, 1):
	# plug subject/part-specific variables into template text
	fsl = template_text
	fsl = re.sub('FEAT_OUTPUT_DIRECTORY', feat_output[i], fsl)
	fsl = re.sub('FEAT_FILE_1', feat_files[i], fsl)
	fsl = re.sub('EV_FILE_1', intersect[i], fsl)
	fsl = re.sub('EV_FILE_2', antic[i], fsl)
	fsl = re.sub('EV_FILE_3', avoid[i], fsl)
	fsl = re.sub('EV_FILE_4', aversive[i], fsl)
	fsl = re.sub('MOTION_FILE', motion[i], fsl)

	# write FSL file
	design_file =  "%s/design_%s_sc2p%d.fsf" % (subject_output[i], subject_id, i + 1)
	with open(design_file, 'w') as f:
		f.write(fsl)

	# create sbatch script
	script = '''
		#!/bin/bash
		#SBATCH --partition=long
		#SBATCH --nodes=1
		#SBATCH --mem-per-cpu=30G
		#SBATCH --time=15:00:00
		#SBATCH --mail-type=ALL
		#SBATCH --mail-user=emily.cohodes@yale.edu
		#SBATCH --workdir=%(work_dir)s
		#SBARCH --job-name=%(job_name)s
		#SBATCH --output=%(work_dir)s/slurm.%%J.log
		#SBATCH --error=%(work_dir)s/slurm.%%J.log
		module load Apps/FSL/5.0.10
		 . /nexsan/apps/hpc/Apps/FSL/5.0.10/etc/fslconf/fsl.sh

		feat %(design_file)s
	''' % {'design_file': design_file, 'work_dir': subject_output[i], 
		'job_name': "feat_%s_p%d" % (subject_id, i + 1)}
	
	# format and save script
	script = re.sub("^\t+", '', script, flags=re.MULTILINE)
	script = re.sub('^\n', '', script)
	script_name = "%s/run_level1_sub_%s_p%d.sh" % (subject_output[i], subject_id, i + 1)
	with open(script_name, 'w') as f:
		f.write(script)
	script_names.append(script_name)

print("The following sbatch scripts have been created:")
for file in script_names:
	print(file)



