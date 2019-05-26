#!/bin/bash
# All tar files should be in a folder.
# This code unpacks each tar file in the folder and deletes the tar file/ 
for file in `ls *.tar`; do tar xf "${file}" && rm "${file}"; done
# This code unzips all of the bz2's in each folder into jsons. 
find -type f -name "*.json.bz2" -exec bunzip2 *.bz2 {} \; 

for i in file1 file2 file3 file4 ; do cat "$i" >> output && rm "$i" || break ; done

find . -type f -exec cat {} + > all.json


