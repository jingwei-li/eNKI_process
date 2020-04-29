
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

for s in subjects:
	sub_dir = BIDS_dir + '/' + s + '/'
	print sub_dir
	sessions = os.walk(sub_dir).next()[1]
	print sessions