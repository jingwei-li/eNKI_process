
# Example:
# python subj_multiple_races.py --ldir /Users/jli/Documents/Research/git_repos/eNKI_process/lists/subjects/ \
#     --lstem 8100_20180806_Race_Sex_Age_Educ_Income --races 1 2 3 4 5 6 DK


import os, sys
import copy
import numpy as np 
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("--ldir", required=True, help="directory to store lists")
parser.add_argument("--lstem", required=True, help="stem of list names")

def_races = "1 2 3 4 5 6 DK"
parser.add_argument("--races", nargs='+', required=True, help="possible races")

args = parser.parse_args()
ldir = args.ldir
lstem = args.lstem
races = args.races
print len(races)


subj_race = []
for race in races:
	print race
	fname = ldir + '/per_race/' + lstem + '_subj_' + str(race) + '.txt'
	f = open(fname, 'r')
	curr_str = f.read()
	f.close()
	curr_list = curr_str.split()
	subj_race.append(curr_list)

subj_race_new = copy.deepcopy(subj_race)
for i in range(0, len(races)-1):
	subj_1 = subj_race[i]
	for j in range(i+1, len(races)):
		subj_2 = subj_race[j]
		comm_subj = np.intersect1d(subj_1, subj_2)
		print "Subjects with both races of ", races[i], ", ", races[j], ": "
		print "    ", comm_subj 

		if len(comm_subj) > 0:
			if (i == 2 and j != 4) or (i == 4 and j != 2):
				subj_race_new[i] = np.setdiff1d(subj_race_new[i], comm_subj)
				print subj_race[i], len(subj_race[i])
				print subj_race_new[i], len(subj_race_new[i])
			elif (j == 2 and i != 4) or (j == 4 and i != 2):
				subj_race_new[j] = np.setdiff1d(subj_race_new[j], comm_subj)
				print subj_race[j], len(subj_race[j])
				print subj_race_new[j], len(subj_race_new[j])
			elif (i == 2 and j == 4) or (i == 4 and j == 2):
				subj_race_new[i] = np.setdiff1d(subj_race_new[i], comm_subj)
				subj_race_new[j] = np.setdiff1d(subj_race_new[j], comm_subj)
				print subj_race[i], len(subj_race[i])
				print subj_race_new[i], len(subj_race_new[i])
				print subj_race[j], len(subj_race[j])
				print subj_race_new[j], len(subj_race_new[j])
			else:
				subj_race_new[j] = np.setdiff1d(subj_race_new[j], comm_subj)
				print subj_race[j], len(subj_race[j])
				print subj_race_new[j], len(subj_race_new[j])


for i in range(0, len(races)):
	race = races[i]
	fname = ldir + '/per_race/' + lstem + '_subj_' + str(race) + '.txt'
	fname_orig = ldir + '/per_race/' + lstem + '_subj_orig_' + str(race) + '.txt'
	if not np.array_equal(np.array(subj_race_new[i]), np.array(subj_race[i])):
		shutil.copyfile(fname, fname_orig)
		f = open(fname, 'w')
		strout = '\n'.join(subj_race_new[i])
		f.write(strout + '\n')
		f.close()
