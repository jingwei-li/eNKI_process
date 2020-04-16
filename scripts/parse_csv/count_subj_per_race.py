##############################################
# Author: Jingwei Li
# Apr. 2020
##############################################

# Example 1:
# python count_subj_per_race.py --sl \
#     ~/Documents/Research/git_repos/eNKI_process/lists/subjects/8100_20180806_Race_Sex_Age_Educ_Income_subj.txt \
#     --csv_dir /Users/jli/Documents/Research/Datasets/eNKI/COINS_assessment_data_20180806

# Example 2:
# python count_subj_per_race.py --sl \
#     ~/Documents/Research/git_repos/eNKI_process/lists/subjects/8100_20180806_Race_Sex_Age_Income_subj.txt \
#     --csv_dir /Users/jli/Documents/Research/Datasets/eNKI/COINS_assessment_data_20180806

import count_subj_categorical as cs 
import numpy as np
import os, sys
import argparse
from unique import unique

parser = argparse.ArgumentParser()
parser.add_argument("--sl", required=True, help="input subject list")
parser.add_argument("--csv_dir", required=True, help="directory storing demographic csv")

def_csv = '8100_Demos_20180806.csv'
help_msg = "relative filename of csv (default is " + def_csv + ")"
parser.add_argument("--csv_name", default=def_csv, help=help_msg)

parser.add_argument("--subj_hdr", default='ID', \
	help="header of subject ID column in csv (default is ID)")
parser.add_argument("--race_hdr", default='DEM_004', \
	help="header of race column in csv (default is DEM_004)")

args = parser.parse_args()
subj_list = args.sl
csv_dir = args.csv_dir
csv_name = csv_dir + '/' + args.csv_name

sl_base = os.path.basename(subj_list)
sl_base = sl_base.strip('.txt')
list_dir = os.path.dirname(subj_list)
outdir = list_dir + '/per_race/'
if not os.path.exists(outdir):
	os.makedirs(outdir)

uniq_race, s_per_race, idx_per_race, counts = cs.count_subj_categorical(fcsv=csv_name, \
	subj_ls=subj_list, subj_hdr=args.subj_hdr, cat_hdr=args.race_hdr, delim=',')
print counts
print range(0, len(uniq_race))

for i in range(0, len(uniq_race)):
	fname = outdir + sl_base + '_' + str(uniq_race[i]) + '.txt'
	print fname
	f = open(fname, 'w')
	list_out = unique(s_per_race[i])
	list_out.sort()
	str_w = '\n'.join(list_out)
	if str_w:
		str_w = str_w + '\n'
	f.write(str_w)
	f.close()
