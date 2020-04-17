
import grab_subj_per_test as gspt

csv_dir = '/Users/jli/Documents/Research/Datasets/eNKI/COINS_assessment_data_20180806'
ls_dir = '/Users/jli/Documents/Research/git_repos/eNKI_process/lists'
subj_ls_stem = 'Race_Sex_Age_Educ_Income'
tests_ls = ls_dir + '/phenotypes/all_test_names.txt'

# f = open(tests_ls, 'r')
# tests = f.read()
# tests = tests.split()
# print tests

# for test in tests:
# 	print test
# 	tot_Nsubj, Nsubj_uniq, subjects, subj_multi_stu, studies, studies_uniq, Nsubj_per_study = \
# 		gspt.get_subjects(csv_dir=csv_dir, ls_dir=ls_dir, test=test, subj_ls_stem=subj_ls_stem)
# 	print tot_Nsubj, Nsubj_uniq, len(subj_multi_stu)
# 	print studies_uniq
# 	print Nsubj_per_study

# 	gspt.write_subj_list(ls_dir, test, subj_ls_stem, subjects, studies)

Demo_ls = ls_dir + '/phenotypes/all_Demo_names.txt'
f = open(Demo_ls, 'r')
Demos = f.read()
Demos = Demos.split()
print Demos

for demo in Demos:
	print demo
	tot_Nsubj, Nsubj_uniq, subjects, subj_multi_stu, studies, studies_uniq, Nsubj_per_study = \
		gspt.get_subjects(csv_dir=csv_dir, ls_dir=ls_dir, test=demo, subj_ls_stem=subj_ls_stem)
	print tot_Nsubj, Nsubj_uniq, len(subj_multi_stu)
	print studies_uniq
	print Nsubj_per_study

	gspt.write_subj_list(ls_dir, demo, subj_ls_stem, subjects, studies)