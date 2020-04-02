##############################################
# Author: Jingwei Li
# Mar. 2020
##############################################

import pandas as pd
import numpy as np
import os, sys

# function to read text file, separated by "delim"
# columns are filtered based on "keep_hdrs"
# rows are filtered based on "rowfilter_hdr" & "rowfilter_list"
def JWL_parse_delimited_file(fname, keep_hdrs=None, rowfilter_hdr=None, rowfilter_list=None, delim=','):
    # fname: abs path of csv file
    # keep_hdrs: list of header names you want to keep
    # rowfilter_hdr: string, header name you want to use to select rows
    # rowfilter_list: string, text file name
    #
    # Example:
    # >>> from grab_subj_Race_Sex_Age_Qualify import JWL_parse_delimited_file
    # >>> tmp = JWL_parse_delimited_file(fname='/home/homeGlobal/jli/my_projects/datasets/UK-Biobank/csv/ukb40471_31_21003_6138_738_709_imgv.csv', keep_hdrs=['eid', '31-0.0', 'Race'], rowfilter_hdr='eid', rowfilter_list='tmp_eid_list')

    X = pd.read_csv(fname, sep=delim, header=None, low_memory=False)
    # many eNKI csv files have two rows of headers, remove the first row
    if X.iat[1,0] == 'ID':
        X = X.drop([0], axis=0)
        X.index = range(X.shape[0])

    # replace column indices with headers
    X.columns = X.iloc[0,:]

    # selected desired columns
    if keep_hdrs is not None:
        X_keep = X[keep_hdrs]
    else:
        X_keep = X
    
    # selected desired rows based the criterion given by rowfilter_hdr & rowfilter_list
    if rowfilter_hdr is not None:
        filter_col = X[rowfilter_hdr]

        if rowfilter_list is None:
            print "rowfilter_list is not passed in!"
            return
        else:
            if isinstance(rowfilter_list, list):
                rowfilter = rowfilter_list
            else:
                rowfilter = []
                with open(rowfilter_list, 'r') as file:
                    for line in file.read().splitlines():
                        rowfilter.append(line)
                file.close()

            filter_ind = filter_col.isin(rowfilter)
            X_keep = X_keep.loc[filter_ind]

    return X_keep

# function to count how many subjects have non-empty values of given columns "filter_hdr"
# the list of subjects with non-empty values are output to "out_txt"
# if multiple filter_hdr is given, output the intersectional set of subjects
def JWL_count_subj_nonempty_intersect(df, subj_hdr, filter_hdr, out_txt=None):
    # df: dataframe structure, contains the information read from a csv file
    #     (see JWL_parse_delimited_file() )
    # subj_hdr: string, header name of subject ID column
    # filter_hdr: string or a list of strings, 
    #             header names to justify which subjects are kept
    #             If multiple headers are passed in, the output will be the conjunction 
    #             of subjects with all corresponding values non-empty
    # out_txt: string, the abs path of output subject list

    try:
        hdr_col = df[filter_hdr]
    except:
        print('df does not contain a column called ',  filter_hdr)
        return
    
    empty_idx = np.where(pd.isnull(hdr_col))
    allrows_idx = np.arange(2, hdr_col.shape[0], 1, dtype=None)
    nonempty_idx = np.setdiff1d(allrows_idx, empty_idx)
    subj_keep = df.loc[nonempty_idx, subj_hdr]
    
    if out_txt is not None:
        subj_keep.to_csv(out_txt, sep=' ', index=False)

    nsubj_keep = len(nonempty_idx)
    return nsubj_keep

# function to count how many subjects have non-empty values of given columns "filter_hdr"
# the list of subjects with non-empty values are output to "out_txt"
# if multiple filter_hdr is given, output the union of subjects
def JWL_count_subj_nonempty_union(df, subj_hdr, filter_hdr, out_txt=None):
    # df: dataframe structure, contains the information read from a csv file
    #     (see JWL_parse_delimited_file() )
    # subj_hdr: string, header name of subject ID column
    # filter_hdr: string or a list of strings, 
    #             header names to justify which subjects are kept
    #             If multiple headers are passed in, the output will be the conjunction 
    #             of subjects with all corresponding values non-empty
    # out_txt: string, the abs path of output subject list

    try:
        hdr_col = df[filter_hdr]
    except:
        print('df does not contain a column called ', filter_hdr)
        return
    
    nonempty_bool = pd.notnull(hdr_col)
    nonempty_bool = nonempty_bool.any(axis=1)
    subj_keep = df.loc[nonempty_bool, subj_hdr]
    subj_keep = subj_keep[1:]
    keep_list = subj_keep.values.to_list()
    print keep_list
    keep_list = keep_list[0]
    print keep_list

    if out_txt is not None:
        subj_keep.to_csv(out_txt, sep=' ', index=False)

    nsubj_keep = subj_keep.shape[0]
    return nsubj_keep