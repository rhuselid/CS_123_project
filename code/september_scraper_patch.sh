#!/bin/bash

# the origional script had an error that meant that september tweets were not downloaded--this is a quick patch
# to download those missing tweets.

base_url="https://archive.org/download/archiveteam-twitter-stream-2018-" #10/twitter-2018-10-01.tar
extension="/twitter-2018-"
zero_extension="/twitter-2018-"
dash='-'
mon='09'
tar='.tar'

for day in `seq 1 30`; do
	if [ $day -lt 10 ]; then
		clean_day="0$day"
	else
		clean_day="$day"
	fi
	echo "$base_url$mon$extension$mon$dash$clean_day$tar"
	wget "$base_url$mon$extension$mon$dash$clean_day$tar"

done

# for day in `seq 1 30`; do wget "https://archive.org/download/archiveteam-twitter-stream-2018-09/twitter-2018-09-0$day$tar"