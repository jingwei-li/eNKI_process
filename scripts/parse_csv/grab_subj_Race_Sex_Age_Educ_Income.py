##############################################
# Author: Jingwei Li
# Apr. 2020
##############################################

import pandas as pd
import numpy as np
import os, sys
import grab_subj_from_csv as gs
from unique import unique

# set directory storing all csv files
ddir = sys.argv[1]
if not ddir.strip():
	ddir = '/data/BnB3/RETRO/T1_DB/DATA/METADATA/eNKI/COINS_assessment_data_20180806' 

s_hdr = 'ID'
git_dir = '/Users/jli/Documents/Research/git_repos/eNKI_process'
odir = git_dir + '/lists'
if not os.path.exists(odir):
    os.makedirs(odir)
ostem = '8100_20180806_'

all_demos = []
all_otxt = []

# Race, Sex, Age
fn = ddir + '/8100_Demos_20180806.csv'
fil_hdr = ['DEM_004', 'DEM_002', 'DEM_001']
all_demos.append(fil_hdr)
fil_hdr_concat = '_'.join(fil_hdr)
o_txt = odir + '/' + ostem + fil_hdr_concat + '_subj.txt'
all_otxt.append(o_txt)
df = gs.JWL_parse_delimited_file(fn)
count = gs.JWL_count_subj_nonempty_intersect(df, subj_hdr=s_hdr, filter_hdr=fil_hdr, out_txt=o_txt)

f = open(o_txt, 'r')
str_in = f.read()
f.close()
list_in = str_in.split('\n')
list_in.pop(-1)
list_out = unique(list_in)
str_out = '\n'.join(list_out)
fw = open(o_txt, 'w')
fw.write(str_out + '\n')
fw.close()
count = len(list_out)
print "# subjects with race, sex, age recorded: ", count

# Education (Adults)
fn = ddir + '/8100_SES-Adult_20180806.csv'
fil_hdr = ['NKISES_01A']
all_demos.append(fil_hdr)
o_txt = odir + '/' + ostem + fil_hdr[0] + '_Adult' + '_subj.txt'
all_otxt.append(o_txt)
df = gs.JWL_parse_delimited_file(fn)
count = gs.JWL_count_subj_nonempty_intersect(df, subj_hdr=s_hdr, filter_hdr=fil_hdr, out_txt=o_txt)

f = open(o_txt, 'r')
str_in = f.read()
f.close()
list_in = str_in.split('\n')
list_in.pop(-1)
list_out = unique(list_in)
str_out = '\n'.join(list_out)
fw = open(o_txt, 'w')
fw.write(str_out + '\n')
fw.close()
count = len(list_out)
print "# adults with education recorded: ", count

# household
fn = ddir + '/8100_Demos-supplement_(2-12-13)_20180806.csv'
fil_hdr = ['DEMOS_02', 'DEMOS_04']
all_demos.append(fil_hdr)
fil_hdr_concat = '_'.join(fil_hdr)
o_txt = odir + '/' + ostem + fil_hdr_concat + '_subj.txt'
all_otxt.append(o_txt)
df = gs.JWL_parse_delimited_file(fn)
count = gs.JWL_count_subj_nonempty_intersect(df, subj_hdr=s_hdr, filter_hdr=fil_hdr, out_txt=o_txt)

f = open(o_txt, 'r')
str_in = f.read()
f.close()
list_in = str_in.split('\n')
list_in.pop(-1)
list_out = unique(list_in)
str_out = '\n'.join(list_out)
fw = open(o_txt, 'w')
fw.write(str_out + '\n')
fw.close()
count = len(list_out)
print "# adults with household income recorded: ", count

# combine demographic criterion
c = 0
for flist in all_otxt:
	c += 1
	f = open(flist, 'r')
	str_in = f.read()
	f.close()

	curr_list = str_in.split('\n')
	curr_list.pop(-1)
	if c==1:
		list_in = curr_list
	else:
		list_in = np.intersect1d(list_in, curr_list)
	print len(list_in)

list_out = unique(list_in)
print all_demos
all_demos = [item for sublist in all_demos for item in sublist]
print all_demos
all_demos_concat = '_'.join(all_demos)
fw_txt = odir + '/' + ostem + all_demos_concat + '_subj.txt'
fw = open(fw_txt, 'w')
str_out = '\n'.join(list_out)
fw.write(str_out + '\n')
fw.close()
count = len(list_out)
print "# subjects with race, sex, age, education, household income recorded: ", count
