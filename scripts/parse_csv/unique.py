##############################################
# Author: Jingwei Li
# Mar. 2020
##############################################

def unique(list_in, silent=True):
	list_set = set(list_in)
	list_out = (list(list_set))

	if not silent:
		for x in list_out:
			print x,

	return list_out
