##############################################
# Author: Jingwei Li
# Apr. 2020
##############################################

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def JWL_histogram(X, bins=None, range=None, outname=None, color=None, title=None, \
	xlabel=None, ylabel=None, legend=None, tick_fontsz=15, label_fontsz=17, title_fontsz=17, \
	display=True, auto_close=False, normed=False):

	# pre-setup
	if bins is None:
		bins = 'auto'
	if color is None:
		color = '#607c8e'
	if tick_fontsz is not None:
		matplotlib.rc('xtick', labelsize=tick_fontsz)
		matplotlib.rc('ytick', labelsize=tick_fontsz)

	# plot
	n, bins, patches = plt.hist(x=X, bins=bins, color=color, alpha=0.7, rwidth=0.9, normed=normed)

	# decorate plot
	if title is not None:
		plt.title(title, fontsize=title_fontsz)

	if xlabel is not None:
		plt.xlabel(xlabel, fontsize=label_fontsz)

	if ylabel is not None:
		plt.ylabel(ylabel, fontsize=label_fontsz)

	if legend is not None:
		plt.legend(legend, frameon=False, loc='best')


	# save figure
	plt.grid(axis='y', alpha=0.75)
	if outname is not None:
		plt.savefig(outname)
	
	# display
	if display:
		if auto_close:
			plt.show(block=False)
			plt.pause(3)
			plt.close()
		else:
			print '[JWL_histogram]: Plese close the window by yourself ...'
			plt.show()
	plt.close()

	