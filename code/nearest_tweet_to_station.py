import json
import pandas as pd
# from mrjob.job import MRJob
import numpy as np
# import csv



with open('sentiment_analyzed.json') as tweet_data:
	for tweet_line in tweet_data:
		with open('US_temperature.json') as tempData:
			for temp_line in tempData:
				tw_latitude, tw_longitude = tweet_line["coordinates"]['coordinates']
				tw_date = tweet_line["date"]["date"]
				temp = temp_line["average_temp"]
				temp_date = temp_line["date"]
				temp_lat = temp_line["latitude"]
				temp_long = temp_line["longitude"]
				station_id = temp_line["station_id"]
				if temp_date == tw_date:
					storage_dict = {}
					max_dist = 0
					distance = np.sqrt((tw_latitude-temp_lat)^2 + (tw_longitude-temp_long)^2)
					if distance > max_dist:
						storage_dict[tweet_line] = (station_id, temp)
						max_dist = distance



# class NearestNeighbor(MRJob):
# # # 		sentiment 
# # tweet_data = json.dumps(tweet_data)
# # print(tweet_data)
# # json.load("sentiment_analyzed.json")
# # class NearestNeighbor(MRJob):
#     def mapper(self, _, line):
#     	# print(line)
#     	line = json.loads(line)
#     	print(line)
	    
# 		# avg = 0.0
# 		# lines = lines.strip()
# 		# features = lines.split(',')
# 		# for i in range(len(features)-1):
# 		# 	if features[i]!='':
# 		# 		avg += (float(features[i]) - float(inputval[i]))**2
# 		# 		dist = math.sqrt(avg)
# 		# 		features.append(str(dist))
# 		# 	print ','.join(features)

#     def combiner(self, num_obs, values):
#     	print("Hello")

#     def reducer(self, num_obs, values):
#     	print("Hello")

# if __name__ == '__main__':
#   NearestNeighbor.run()