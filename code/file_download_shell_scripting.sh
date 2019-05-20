#!/bin/bash

# script to download the twitter data (a bunch of jsons) and then turn this into
# a single file.

base_url="https://archive.org/details/archiveteam-twitter-stream-2018-" #10/twitter-2018-10-01.tar
extension="/twitter-2018-"
dash='-'
tar='.tar'

for m in `seq 1 10`; do
	if [ $m -eq 1 -o $m -eq 3 -o $m -eq 5 -o $m -eq 7 -o $m -eq 8 $m -eq 10 ]; then
		for day in `seq 1 31`; do

			if [ day -lt 10 ]; then
				clean_day="'0'$day"
			else
				clean_day="$day"
			fi

			if [ $m -lt 10 ]; then
				mon="'0'$m"
				wget "$base_url$mon$extension$mon$dash$clean_day$tar"
				# -01 has a leading 0
			else
				mon=$m
				wget $base_url + $mon + $extension + $mon + '-' + clean_day + '.tar'
				# -10 has no leading 0
			fi
		done
	elif [ $m -eq 4 -o $m -eq 6 -o $m -eq 9 ]; then
		for day in `seq 1 30`; do
			if [ day -lt 10 ]; then
				clean_day=0 + day
			else
				clean_day=day
			fi

			wget $base_url + $m + $extension + $m + '-' + clean_day + '.tar'

		done
	else
		for day in `seq 1 28`; do
			if [ day -lt 10 ]; then
				clean_day="0$day"
			else
				clean_day="day"
			fi

			wget $base_url + $m + $extension + $m + '-' + clean_day + '.tar'
		done
	fi
done
