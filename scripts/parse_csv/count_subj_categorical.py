##############################################
# Author: Jingwei Li
# Mar. 2020
##############################################

import pandas as pd
import numpy as np
import os, sys
from grab_subj_from_csv import JWL_parse_delimited_file
from unique import unique

def count_subj_categorical(fcsv, subj_ls, subj_hdr, cat_hdr, delim=','):
    # Given the header of a categorical column in the "fcsv" file, this function 
    # calculates the number of subject based on each unique value of that column
    #
    # fcsv:	
    #     string, abs path of csv file containing the necessary phenotypical information
    # subj_ls: 
    #     list of subject IDs. Each line corresponds to one subject
    # subj_hdr: 
    #     header name of subject ID column
    # cat_hdr: 
    #     header name of the categorical column 
    # delim (optional):
    #     delimiter of fcsv. Default is ','
    #
    # ------ Outputs ------ #
    # uniq:
    #     list, unique values of the "cat_hdr" column
    # sgroups:
    #     list of lists. Each sub-list contains the subjects with the same value in 
    #     "cat_hdr" column
    # idx:
    #     list of lists. Each sub-list contains the index of the corresponding subjects 
    #     in "sgroups". 
    # counts:
    #     list, the number of subjects per group


    X_keep = JWL_parse_delimited_file(fname=fcsv, keep_hdrs=None, rowfilter_hdr=subj_hdr, rowfilter_list=subj_ls)

    # get unique values of the given categorical column
    cat_col = X_keep[cat_hdr]
    cat_list = cat_col.tolist()
    uniq = unique(cat_list)

    # find which subject corresponds to which unique value
    subj_col = X_keep[subj_hdr]
    subj_list = subj_col.tolist()
    idx = []
    sgroups = []
    counts = []
    for x in uniq:
    	curr_idx = [i for i in range(len(cat_list)) if cat_list[i]==x]
    	idx.append(curr_idx)
    	sgroups.append(np.array(subj_list)[curr_idx])
    	counts.append(len(curr_idx))

    return uniq, sgroups, idx, counts;
