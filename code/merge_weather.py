
import csv
import pandas as pd
import json
import numpy as np

top = 49.3457868 # north lat
bottom =  24.7433195 # south lat
left = -124.7844079 # west long
right = -66.9513812 #east long

weatherdata = pd.read_csv("2018.csv")
w_cols = ["stationid", "date", "weathertype", "quantity","empty1", "empty2", "empty3", "empty4"]
weatherdata.columns=w_cols

stationdata = pd.read_fwf("stations.txt")
s_cols = ["stationid", "latitude", "longitude", "elevation","location", "empty1", "empty2", "empty3"]
stationdata.columns=s_cols
merged = pd.merge(weatherdata, stationdata, on='stationid', how='left')
merge_dropped = merged.drop(["empty1_x", "empty2_x", "empty3_x", "empty1_y", "empty2_y", "empty3_y", "empty4"], axis=1)

temperature_type = ["TMIN", "TMAX"]
temp = merge_dropped[merge_dropped['weathertype'].isin(temperature_type)]
temp_avg = temp.groupby(["stationid", "date"]).quantity.mean()
temp_df = temp_avg.to_frame().reset_index()

temp_df_merge = pd.merge(temp_df, stationdata, on="stationid", how="left").drop(["empty1", "empty2", "empty3", "elevation"], axis=1)
temp_df_merge.rename(columns={'quantity':'average_temp'}, inplace=True)

US_temp_df = temp_df_merge[(temp_df_merge['latitude'] > bottom) & (temp_df_merge['latitude'] < top)]
US_temp_df = US_temp_df[(US_temp_df['longitude'] > left) & (US_temp_df['longitude'] < right)]


US_temp_df["month"] = np.floor_divide(np.remainder(US_temp_df["date"], 10000), 100)
df_October = US_temp_df.loc[US_temp_df["month"] == 10]
df_October.to_csv("October_temperature.csv")
# 
# print(US_temp_df["date"][4:6])

# print(US_temp_df)
# # jsonfilepath = "US_temperature.json"
# jsonfile = open('US_temperature.json', 'w')
# US_temp_df.to_csv("US_temperature.csv")

# # data = {}
# with open("US_temperature.csv") as csvFile:
# 	csvReader = csv.DictReader(csvFile)
# 	for csvRow in csvReader:
# 		json.dump(csvRow, jsonfile)
# 		jsonfile.write('\n')
		# json.dump(csvRow, )
		# stationid = csvRow["stationid"]
		# date = csvRow["date"]
		# key = stationid + date
		# data[key] = csvRow
    	# json.dump(csvRow, jsonfile)
    	# jsonfile.write('\n')

# data = [data]

# with open(jsonfilepath, "w") as f:
# 	f.write('\n'.join(json.dumps(i) for i in data) + '\n')
# with open(jsonfilepath, "w") as jsonFile:
# 	s = json_dumps
# 	jsonFile.write(json.dumps(data, indent=4))


# A = US_temp_df.to_json("US_temperature.json")

# for index, row in merge_dropped.itterows():
# 	if row.
# 	print(index, row)

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