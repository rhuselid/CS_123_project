#!/bin/bash

# script to download the twitter data (a number of tar files from archive.org).

# it takes roughly 30 hours for this script to run. Their servers are based in San Francisco,
# so we found that renting VMs from LA to be the most time-efficient (we ended up repeating 
# this process multiple times). 

base_url="https://archive.org/download/archiveteam-twitter-stream-2018-" #10/twitter-2018-10-01.tar
extension="/twitter-2018-"
zero_extension="/twitter-2018-0"
dash='-'
tar='.tar'

for m in `seq 1 10`; do
	if [ $m -lt 5 ]; then
		# the urls are formated differently Jan-Apr
		# example: https://archive.org/download/archiveteam-twitter-stream-2018-02/archiveteam-twitter-stream-2018-02.tar
		mon="0$m"
		echo "$base_url$mon/archiveteam-twitter-stream-2018-$mon.tar"
		wget "$base_url$mon/archiveteam-twitter-stream-2018-$mon.tar"
	
	elif [ $m -eq 5 -o $m -eq 7 -o $m -eq 8 -o $m -eq 10 ]; then

		for day in `seq 1 31`; do
			echo $day
			if [ $day -lt 10 ]; then
				clean_day="0$day"
			else
				clean_day="$day"
			fi

			if [ $m -lt 10 ]; then
				mon="0$m"
				# -01 has a leading 0
			else
				mon=$m
				# -10 has no leading 0
			fi
			echo "$base_url$mon$extension$mon$dash$clean_day$tar"
			wget "$base_url$mon$extension$mon$dash$clean_day$tar"
		done

	elif [ $m -eq 6 -o $m -eq 9 ]; then
		for day in `seq 1 30`; do
			if [ $day -lt 10 ]; then
				clean_day="0$day"
			else
				clean_day="$day"
			fi
			mon="0$m"
			echo "$base_url$mon$extension0$m$dash$clean_day$tar"
			wget "$base_url$mon$extension0$m$dash$clean_day$tar"

		done
	fi

	# febuary no longer necessary because I realized the Jan-Apr tars were formated differently

	# else
	# 	# febuary
	# 	for day in `seq 1 28`; do
	# 		if [ $day -lt 10 ]; then
	# 			clean_day="0$day"
	# 		else
	# 			clean_day="day"
	# 		fi
	# 		echo "$base_url$m$extension$mon$dash$clean_day$tar"
	# 		wget "$base_url$m$extension$mon$dash$clean_day$tar"
	# 	done
	# fi
done
