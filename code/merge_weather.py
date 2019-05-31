# import pandas as pd
import csv
# print("Lebron sucks")
import pandas as pd
print("Lebron sucks")
weatherdata = pd.read_csv("2018.csv")
w_cols = ["stationid", "date", "weathertype", "quantity","empty1", "empty2", "empty3", "empty4"]
weatherdata.columns=w_cols
# print(weatherdata[:10])
stationdata = pd.read_fwf("stations.txt")
s_cols = ["stationid", "latitude", "longitude", "elevation","location", "empty1", "empty2", "empty3"]
stationdata.columns=s_cols
merged = pd.merge(weatherdata, stationdata, on='stationid', how='left')
# print(stationdata[:10])

# https://stackoverflow.com/questions/35063137/how-to-rename-key-header-in-csv-dictreader

# path = "2018.csv"
# file = open(path, newline="")

# with open('weatherdata/2018.csv') as infd, open('weatherdata/2018_final.csv', 'w') as outfd:
#   reader = csv.reader(infd)
#   writer = csv.writer(outfd)

#   # read the header
#   header = next(reader)

#   # modify the column title
#   header = ["stationid", "date", "weathertype", "quantity",
#    "empty1", "empty2", "N_or_a"]

#   # write the new header out
#   writer.writerow(header)

#   # copy all other rows unmodified
#   for row in reader:
#     writer.writerow(row)

# count = 0
# for line in open("2018_final.csv"):
# 	if count>10:
# 		break
# 	else:
# 		print(count)
# 		print(line)
# 		count+=1

# with open('station.txt', 'r') as f:
# 	f_contents = f.readline()
# 	print(f_contents)

# 	f_contents = f.readline()
# 	print(f_contents)
# 	# for line in f:
# 	# 	print(line, end=" ")