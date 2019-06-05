import csv
import pandas as pd
import json
import numpy as np

'''
Merges the station data with the weatherdata while dropping all unnecesary cols.
Also, minimizes dataset by only including the lats, longs of the continental US. 
The temp was given in Celsius but the NOAA measured it by the 100s (i.e. 200 C
= 20 C). Therefore, the temp is divided by 10. Last, the dataset was specified 
for the month of October. 
'''
top = 49.3457868 # north lat
bottom =  24.7433195 # south lat
left = -124.7844079 # west long
right = -66.9513812 #east long

weatherdata = pd.read_csv("2018.csv")
w_cols = ["stationid", "date", "weathertype", "quantity","empty1", "empty2", 
			"empty3", "empty4"]
weatherdata.columns=w_cols

stationdata = pd.read_fwf("stations.txt")
s_cols = ["stationid", "latitude", "longitude", "elevation","location", "empty1"
		, "empty2", "empty3"]
stationdata.columns=s_cols
merged = pd.merge(weatherdata, stationdata, on='stationid', how='left')
merge_dropped = merged.drop(["empty1_x", "empty2_x", "empty3_x", "empty1_y", 
							"empty2_y", "empty3_y", "empty4"], axis=1)

temperature_type = ["TMIN", "TMAX"]
temp = merge_dropped[merge_dropped['weathertype'].isin(temperature_type)]
temp_avg = temp.groupby(["stationid", "date"]).quantity.mean()
temp_df = temp_avg.to_frame().reset_index()

temp_df_merge = pd.merge(temp_df, stationdata, on="stationid", how="left").drop(["empty1", "empty2", "empty3", "elevation"], axis=1)
temp_df_merge.rename(columns={'quantity':'average_temp'}, inplace=True)

US_temp_df = temp_df_merge[(temp_df_merge['latitude'] > bottom) & 
							(temp_df_merge['latitude'] < top)]

US_temp_df = US_temp_df[(US_temp_df['longitude'] > left) & 
			(US_temp_df['longitude'] < right)]

US_temp_df["average_temp"] = (US_temp_df["average_temp"])/10 #Temp data was incorrectly calculated

US_temp_df["month"] = np.floor_divide(np.remainder(US_temp_df["date"], 10000), 100) #Establishes the month for each temp

df_October = US_temp_df.loc[US_temp_df["month"] == 10]

df_October.to_csv("October_temperature.csv")
