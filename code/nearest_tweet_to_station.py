import json
import numpy as np
import pandas as pd
from mrjob.job import MRJob
from datetime import datetime
from dateutil.parser import parse
import random
import csv

# with open('sentiment_analyzed.json') as json_data:
# 	# data = json.load(json_data)
# 	for line in json_data:
# 		line = json.loads(line)
# 		latitude, longitude = line["coordinates"]['coordinates']

# 		print(latitude, longitude)

class NearestNeighbor(MRJob):
# # 		sentiment 
# tweet_data = json.dumps(tweet_data)
# print(tweet_data)
# json.load("sentiment_analyzed.json")
# class NearestNeighbor(MRJob):
    def mapper(self, _, line):
    	print(line)
    	# line = json.loads(line)
    	# print(line)
    	# with open('sentiment_analyzed.json') as json_data:
	    # 	for line in json_data:
	    # 		print(line)
	    
				# avg = 0.0
				# lines = lines.strip()
				# features = lines.split(',')
				# for i in range(len(features)-1):
				# 	if features[i]!='':
				# 		avg += (float(features[i]) - float(inputval[i]))**2
				# 		dist = math.sqrt(avg)
				# 		features.append(str(dist))
				# 	print ','.join(features)

    def combiner(self, num_obs, values):
    	print("Hello")

    def reducer(self, num_obs, values):
    	print("Hello")

if __name__ == '__main__':
  NearestNeighbor.run()