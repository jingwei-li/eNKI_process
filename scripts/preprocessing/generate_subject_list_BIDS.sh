#!/bin/bash

BIDS_dir="/data/BnB1/Raw_Data/eNKI_BIDS"
regex=^sub-A[0-9]{8}$
folders=$(find $BIDS_dir -mindepth 1 -maxdepth 1 -type d)

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
out_dir=$(dirname $(dirname $script_dir))

subjects=
for f in $folders; do
	bname=$(basename $f)
	if [[ $bname =~ $regex ]]; then
		subjects="$subjects $bname"
	fi
done

out_list="${out_dir}/lists/subjects/subjects_BIDS.txt"
rm $out_list
for s in $subjects; do
    echo $s >> $out_list
done
