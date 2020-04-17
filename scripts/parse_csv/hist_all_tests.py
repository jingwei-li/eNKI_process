import hist_per_test as hpt


csv_dir = '/Users/jli/Documents/Research/Datasets/eNKI/COINS_assessment_data_20180806'
ls_dir = '/Users/jli/Documents/Research/git_repos/eNKI_process/lists'

subj_ls_stem = 'Race_Sex_Age_Educ_Income'
fig_dir = '/Users/jli/Documents/Research/Datasets/eNKI/figures/histograms'
races = ['3', '5']
legends = ['AA', 'WA']

tests_ls = ls_dir + '/phenotypes/all_test_names_min100AA_2.txt'
f = open(tests_ls, 'r')
all_tests = f.read()
f.close()
all_tests = all_tests.split()

for test in all_tests:
	print test
	df = hpt.read_scores(csv_dir, ls_dir, test, subj_ls_stem)
	hpt.hist_population(df, test, ls_dir, subj_ls_stem, fig_dir)
	hpt.hist_2races(df, races, test, ls_dir, subj_ls_stem, legends, fig_dir)
	hpt.hist_2races(df, races, test, ls_dir, subj_ls_stem, legends, fig_dir, True)

# Demos_ls = ls_dir + '/phenotypes/all_Demo_names.txt'
# f = open(Demos_ls, 'r')
# all_Demos = f.read()
# f.close()
# all_Demos = all_Demos.split()

# for demo in all_Demos:
# 	print demo
# 	df = hpt.read_scores(csv_dir, ls_dir, demo, subj_ls_stem)
# 	hpt.hist_population(df, demo, ls_dir, subj_ls_stem, fig_dir)
# 	hpt.hist_2races(df, races, demo, ls_dir, subj_ls_stem, legends, fig_dir)
# 	hpt.hist_2races(df, races, demo, ls_dir, subj_ls_stem, legends, fig_dir, True)