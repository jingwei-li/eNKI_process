
import os, sys, csv, errno
import argparse
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from copy import copy
import grab_subj_from_csv as gs
from unique import unique
from JWL_hist import JWL_histogram

def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def read_scores(csv_dir, ls_dir, test, subj_ls_stem):
	if 'Penn_CNP' in test:
		csvname = csv_dir + '/8100_' + 'Penn_CNP_(12-18-13)' + '_20180806.csv'
	elif test == 'Demos-supplement':
		csvname = csv_dir + '/8100_' + 'Demos-supplement_(2-12-13)' + '_20180806.csv'
	else:
		csvname = csv_dir + '/8100_' + test + '_20180806.csv'
	pheno_ls = ls_dir + '/phenotypes/' + test + '.txt'
	subj_ls = ls_dir + '/subjects/per_test/' + test + '/8100_20180806_' + subj_ls_stem + '_SubjStudy.csv'

	# setup colume filter headers
	subj_hdr = 'ID'
	study_hdr = "SUB_STUDY"
	f = open(pheno_ls, 'r')
	hdr_str = f.read()
	f.close()
	hdr_ls = hdr_str.split()
	hdr_ls.insert(0, study_hdr)
	hdr_ls.insert(0, subj_hdr)

	# read subjects and studies with non-empty data
	subj_study = []
	with open(subj_ls, 'r') as f:
		reader = csv.reader(f, delimiter=',', quotechar='|')
		for row in reader:
			subj_study.append(row)
	subj_study = np.array(subj_study).T.tolist()

	df = gs.JWL_parse_delimited_file_2rowfilters(fname=csvname, keep_hdrs=hdr_ls, \
		rowflt_hdr_ls=[subj_hdr, study_hdr], rowflt_val_ls=subj_study, delim=',')

	return df

def subset_1race(df, race, ls_dir, test, subj_ls_stem):
	subj_hdr = 'ID'
	study_hdr = 'SUB_STUDY'

	pheno_ls = ls_dir + '/phenotypes/' + test + '.txt'
	f = open(pheno_ls, 'r')
	hdr_str = f.read()
	f.close()
	hdr_ls = hdr_str.split()

	race_ls = ls_dir + '/subjects/per_test/' + test + '/8100_20180806_' + subj_ls_stem + '_subj_' + race + '.txt'
	f = open(race_ls, 'r')
	subj_race = f.read()
	f.close()
	subj_race = subj_race.split()
	df_subj_col = df[subj_hdr]
	idx = df_subj_col.isin(subj_race)
	values = df.loc[idx, hdr_ls].values.tolist()   # till here each sub-list corresponds to 1 subject
	# transpose the array so that each sub-list corresponds to 1 measure
	values = np.array(values).T     # returns a numpy array
	return values

def hist_population(df, test, ls_dir, subj_ls_stem, fig_dir):
	outdir = fig_dir + '/' + test
	mkdir_p(outdir)

	# read header names of different measures in current test
	pheno_ls = ls_dir + '/phenotypes/' + test + '.txt'
	f = open(pheno_ls, 'r')
	hdr_str = f.read()
	f.close()
	hdr_ls = hdr_str.split()

	# prepare the values to be plotted
	data = df.loc[:, hdr_ls].values.tolist()
	data = np.array(data).T
	for c in range(0, len(data)):
		# setup output file name
		outname = outdir + '/8100_20180806_' + subj_ls_stem + '_' + hdr_ls[c] + '_pop.png'

		if not os.path.exists(outname):
			print '\t', hdr_ls[c]
			curr_data = data[c]

			print '\t\tConverting values to float'
			float_data = []
			for j in curr_data:
				try:
					float_data.append(float(j))
				except:
					print '\t\t', j, 'cannot be converted to float.'
			#float_data = [float(j) for j in curr_data]
			float_data = np.array(float_data)

			if hdr_ls[c] == 'DKEFSCWI_23':
				float_data = float_data[float_data<2000]
			elif hdr_ls[c] == 'PENNCNP_0210':
				float_data = float_data[float_data<200]

			# check NaN
			if np.isnan(np.sum(float_data)):
				print '\t\tWarning: there are', len(float_data[np.isnan(float_data)]), 'NaNs in current phenotype.'
				float_data = float_data[~np.isnan(float_data)]

			# setup #bins based on the number of unique values
			uniq = unique(float_data)
			if len(uniq) >20:
				bins = 50
			else:
				bins = len(uniq)

			# plotting
			JWL_histogram(X=float_data, bins=bins, outname=outname, title=hdr_ls[c], \
				xlabel='Values', ylabel='# subjects', display=False, auto_close=True)

def hist_2races(df, races, test, ls_dir, subj_ls_stem, legends, fig_dir, normed=False):
	if len(races) != 2:
		sys.exit('This function can only plot for 2 races.')

	if len(legends) != 2:
		sys.exit('Number of legends must be 2.')

	outdir = fig_dir + '/' + test
	mkdir_p(outdir)

	# read header names of different measures in current test
	pheno_ls = ls_dir + '/phenotypes/' + test + '.txt'
	f = open(pheno_ls, 'r')
	hdr_str = f.read()
	f.close()
	hdr_ls = hdr_str.split()

	val1 = subset_1race(df, races[0], ls_dir, test, subj_ls_stem)
	val2 = subset_1race(df, races[1], ls_dir, test, subj_ls_stem)

	for c in range(0, len(hdr_ls)):
		if normed:
			ofname = outdir + '/8100_20180806_' + subj_ls_stem + '_' + hdr_ls[c] + '_' + races[0] + 'vs' + races[1] + '_normed.png'
		else:
			ofname = outdir + '/8100_20180806_' + subj_ls_stem + '_' + hdr_ls[c] + '_' + races[0] + 'vs' + races[1] + '.png'

		if not os.path.exists(ofname):
			print '\t', hdr_ls[c]

			print '\t\tConverting values of race', races[0], 'to float'
			float_val1 = []
			for j in val1[c]:
				try:
					float_val1.append(float(j))
				except:
					print '\t\t', j, 'cannot be converted to float'
			#float_val1 = [float(j) for j in val1[c]]
			float_val1 = np.array(float_val1)
			if hdr_ls[c] == 'DKEFSCWI_23':
				float_val1 = float_val1[float_val1<2000]
			elif hdr_ls[c] == 'PENNCNP_0210':
				float_val1 = float_val1[float_val1<200]

			print '\t\tConverting values of race', races[1], 'to float'
			float_val2 = []
			for j in val2[c]:
				try:
					float_val2.append(float(j))
				except:
					print '\t\t', j, 'cannot be converted to float'
			#float_val2 = [float(j) for j in val2[c]]
			float_val2 = np.array(float_val2)
			if hdr_ls[c] == 'DKEFSCWI_23':
				float_val2 = float_val2[float_val2<2000]
			elif hdr_ls[c] == 'PENNCNP_0210':
				float_val2 = float_val2[float_val2<200]

			if np.isnan(np.sum(float_val1)):
				print '\t\tWarning: there are', len(float_val1[np.isnan(float_val1)]), 'NaNs in race', races[0], 'in current phenotype.'
				float_val1 = float_val1[~np.isnan(float_val1)]

			if np.isnan(np.sum(float_val2)):
				print '\t\tWarning: there are', len(float_val2[np.isnan(float_val2)]), 'NaNs in race', races[1], 'in current phenotype.'
				float_val2 = float_val2[~np.isnan(float_val2)]

			data_plot = [float_val1, float_val2]
			data_flat = np.append(float_val1, float_val2)

			uniq = unique(data_flat)
			if len(uniq) >20:
				bins = 50
			else:
				bins = len(uniq)


			JWL_histogram(data_plot, bins=bins, outname=ofname, color=['#607c8e', '#32a852'], title=hdr_ls[c], \
				legend=legends, display=False, auto_close=True, normed=normed)



