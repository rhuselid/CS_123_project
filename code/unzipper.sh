#!/bin/bash
# All tar files should be in a folder.
# This code unpacks each tar file in the folder
for f in `ls *.tar` ; do
    dir="${f%.*}"
    mkdir "$dir"
    cd $dir
    tar -xf "../$f"
    cd ..
done
# This code enters each folder (made from each tar), navigates down 4 levels, and unzips each bz2 file

for d in ./*/ ; do
    cd *; cd *; cd *; cd *
    for j in ./*/ ; do
      (cd "$j" && bunzip2 *.bz2) done
done



