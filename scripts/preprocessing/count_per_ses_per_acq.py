
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

# collect the subjects who have a certain session code
known_ses.sort()
sub_per_known_ses = [[] for i in range(len(known_ses))]
Nsub_per_known_ses = []

for ks in range(0, len(known_ses)):
	curr_known_ses = known_ses[ks]

	for s_i in range(0, len(subjects)):
		if curr_known_ses in ses_persub[s_i]:
			index = ses_persub[s_i].index(curr_known_ses)
			if ses_anat[s_i][index]:
				sub_per_known_ses[ks].append(subjects[s_i])

	Nsub_per_known_ses.append(len(sub_per_known_ses[ks]))

print Nsub_per_known_ses

# collect subject-session combinations which have a certain acquisition code
known_acq = ['1400', '650', 'cap']
sub_per_ses_acq = []
Nsub_per_ses_acq = np.zeros(len(known_ses), len(known_acq))
for ka in range(0, len(known_acq)):
	sub_per_ses_acq.append([[] for i in range(len(known_ses))])
	for ks in range(0, len(known_ses)):
		curr_subjs = sub_per_known_ses[ks]
		for s in curr_subjs:
			curr_nii = BIDS_dir + '/' + s + '/' + known_ses[ks] + '/func/' + \
				s + '_' + known_ses[ks] + '_task-rest_acq-' + known_acq[ka] + '_bold.nii'
			if os.path.exists(curr_nii):
				sub_per_ses_acq[ka][ks].append(s)
				Nsub_per_ses_acq[ks, ka] += 1

print Nsub_per_ses_acq

