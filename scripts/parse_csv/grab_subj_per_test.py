##############################################
# Author: Jingwei Li
# Apr. 2020
##############################################

import pandas as pd
import numpy as np
import csv
import os, sys
import errno
import grab_subj_from_csv as gs
from unique import unique

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def get_subjects(csv_dir, ls_dir, test, subj_ls_stem):
	if 'Penn_CNP' in test:
		csv = csv_dir + '/8100_' + 'Penn_CNP_(12-18-13)' + '_20180806.csv'
	else:
		csv = csv_dir + '/8100_' + test + '_20180806.csv'
	pheno_ls = ls_dir + '/phenotypes/' + test + '.txt'
	subj_ls = ls_dir + '/subjects/8100_20180806_' + subj_ls_stem + '_subj.txt'
	outdir = ls_dir + '/subjects/per_test/' + test
	mkdir_p(outdir)

	subj_hdr = 'ID'
	study_hdr = "SUB_STUDY"
	f = open(pheno_ls, 'r')
	hdr_str = f.read()
	f.close()
	hdr_ls = hdr_str.split()
	hdr_ls.insert(0, study_hdr)
	hdr_ls.insert(0, subj_hdr)

	df = gs.JWL_parse_delimited_file(fname=csv, keep_hdrs=hdr_ls, rowfilter_hdr=subj_hdr, \
		rowfilter_list=subj_ls, delim=',')
	df.index = range(len(df))
	tot_Nsubj, subj_keep, row_idx = gs.JWL_count_subj_nonempty_intersect(df, subj_hdr, hdr_ls[1:], out_txt=None)

	subj_keep = subj_keep.to_list()
	subj_uniq = unique(subj_keep)
	Nsubj_uniq = len(subj_uniq)

	subj_multi_studies = []
	for s in subj_uniq:
		Nstudy_subj = subj_keep.count(s)
		if Nstudy_subj > 1:
			subj_multi_studies.append(s)

	studies = df.loc[row_idx, study_hdr]
	studies = studies.to_list()
	studies_uniq = unique(studies)
	Nsubj_per_study = []
	for study in studies_uniq:
		Nsubj_study = studies.count(study)
		Nsubj_per_study.append(Nsubj_study)
	return tot_Nsubj, Nsubj_uniq, subj_keep, subj_multi_studies, studies, studies_uniq, Nsubj_per_study


def write_subj_list(ls_dir, test, subj_ls_stem, subjects, studies):
	ls_prep = '8100_20180806_'
	outdata = np.array([subjects, studies])
	outdata = outdata.T.tolist()

	outdir = ls_dir + '/subjects/per_test/' + test
	mkdir_p(outdir)
	outcsv = outdir + '/' + ls_prep + subj_ls_stem + '_SubjStudy.csv'
	outtxt = outdir + '/' + ls_prep + subj_ls_stem + '_UniqSubj.txt'

	with open(outcsv, 'w') as f:
		wr = csv.writer(f)
		wr.writerows(outdata)

	f = open(outtxt, 'w')
	strout = '\n'.join(unique(subjects))
	f.write(strout + '\n')
	f.close()

	# per race
	races = ['1', '2', '3', '4', '5', '6', 'DK']
	for race in races:
		race_ls = ls_dir + '/subjects/per_race/' + ls_prep + subj_ls_stem + '_subj_' + race + '.txt'
		f = open(race_ls, 'r')
		subj_race = f.read()
		subj_race = subj_race.split()
		subj_keep_race = np.intersect1d(subjects, subj_race)

		outtxt = outdir + '/' + ls_prep + subj_ls_stem + '_subj_' + race + '.txt'
		f = open(outtxt, 'w')
		strout = '\n'.join(subj_keep_race)
		if strout:
			strout = strout + '\n'
		f.write(strout)
		f.close()

