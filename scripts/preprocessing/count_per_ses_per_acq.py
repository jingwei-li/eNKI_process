
import os, sys
import numpy as np
import argparse

script_name = os.path.realpath(__file__)
ldir = os.path.abspath(os.path.join(script_name, os.pardir))
ldir = os.path.abspath(os.path.join(ldir, os.pardir))
ldir = os.path.abspath(os.path.join(ldir, os.pardir))
ldir = ldir + '/lists/'

parser = argparse.ArgumentParser()
subj_ls_def = ldir + 'subjects/subjects_BIDS.txt'
parser.add_argument("--subj_ls", default=subj_ls_def, help="subject list")

BIDS_dir_def = '/data/BnB1/Raw_Data/eNKI_BIDS'
parser.add_argument("--BIDS_dir", default=BIDS_dir_def, help="directory to store BIDS format eNKI subjects")

args = parser.parse_args()
subj_ls = args.subj_ls
BIDS_dir = args.BIDS_dir

with open(subj_ls, 'r') as f:
	subjects = f.read()
	subjects = subjects.split()

count = 1
ses_anat = []
ses_persub = []
for s in subjects:
	ses_anat_sub = []
	sub_dir = BIDS_dir + '/' + s + '/'

	sessions = os.walk(sub_dir).next()[1]
	ses_persub.append(sessions)
	for ses in sessions:
		# check if current subject, current session has anat data
		has_anat = os.path.exists(sub_dir + '/' + ses + '/anat')
		ses_anat_sub.append(has_anat)

		# collect all possible session codes, only consider sessions with anat
		if has_anat:
			if count == 1:
				known_ses = [ses]
			else:
				if ses not in known_ses:
					known_ses.append(ses)
			count += 1

	ses_anat.append(ses_anat_sub)

print known_ses
print ses_persub
print ses_anat