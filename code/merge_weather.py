import pandas as pd
import csv

path = "2018.csv"
file = open(path, newline="")

# with open('2018.csv') as infd, open('2018_final.csv', 'w') as outfd:
#   reader = csv.reader(infd)
#   writer = csv.writer(outfd)

#   # read the header
#   header = next(reader)

#   # modify the column title
#   header = ["stationid", "date", "weathertype", "quantity", "empty1", "empty2", "N_or_a"]

#   # write the new header out
#   writer.writerow(header)

#   # copy all other rows unmodified
#   for row in reader:
#     writer.writerow(row)

count = 0
for line in open("2018_final.csv"):
	if count>20:
		break
	else:
		print(count)
		print(line)
		count+=1