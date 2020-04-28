#!/bin/sh

BIDS_dir="/data/BnB1/Raw_Data/eNKI_BIDS"
prefix="sub-A"
regex=^[0-9]{8}$
folders=$(find $BIDS_dir -mindepth 1 -maxdepth 1 -type d)

subjects=
for f in $folders; do
	bname=$(basename $f)
	if [[ $bname =~ $regex ]]; then
		subjects="$subjects $bname"
	fi
done
echo $subjects