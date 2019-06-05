import json
import pandas as pd
from mrjob.job import MRJob
import numpy as np
import datetime

import csv
#Month Dictionary

month_dictionary = {
	"Jan":"01",
	"Feb":"02",
	"Mar":"03",
	"Apr":"04",
	"May":"05",
	"Jun":"06",
	"Jul":"07",
	"Aug":"08",
	"Sep":"09",
	"Oct":"10",
	"Nov":"11",
	"Dec":"12"
}
# open("sentiment_analyzed.json", encoding="iso-8859-1")

# with open('sentiment_analyzed.json') as tweet_data:
# 	for tweet_line in tweet_data:
# 		with open('US_temperature.json') as tempData:
# 			for temp_line in tempData:
# 				tw_latitude, tw_longitude = tweet_line["coordinates"]['coordinates']
# 				tw_date = tweet_line["date"]["date"]
# 				temp = temp_line["average_temp"]
# 				temp_date = temp_line["date"]
# 				temp_lat = temp_line["latitude"]
# 				temp_long = temp_line["longitude"]
# 				station_id = temp_line["station_id"]
# 				if temp_date == tw_date:
# 					storage_dict = {}
# 					max_dist = 0
# 					distance = np.sqrt((tw_latitude-temp_lat)^2 + (tw_longitude-temp_long)^2)
# 					if distance > max_dist:
# 						storage_dict[tweet_line] = (station_id, temp)
# 						max_dist = distance

class NearestNeighbor(MRJob):
# # 		sentiment 
# tweet_data = json.dumps(tweet_data)
# print(tweet_data)
# json.load("sentiment_analyzed.json")
# class NearestNeighbor(MRJob):
    # with open("US_temperature.json") as temperature_data:
        # for data in temperature_data:
        # temp_data = json.load(temperature_data)
        # print(temperature_data)

    def mapper(self, _, line):
        row = json.loads(line)
        date = row["created_at"]
        month = date[4:7]
        month_num = month_dictionary[month] 
        date = date[-4:] + month_num + date[8:10]
        yield date, row

    def combiner_init(self):
        '''
 
        '''
        # self.temperature_data = json.loads(temperature)

        self.temp_data = pd.read_csv(r"October_temperature.csv")
        col_names = ["empty1","station_id", "date","temp", "lat", "long", "location", "month"]
        self.temp_data.columns=col_names

    def combiner(self, date, tweets):
        for tweet in tweets:
            min_dist = 1000000
            tweet_lat, tweet_long = tweet["coordinates"]["coordinates"]
            for data in self.temp_data.iterrows():
                temp_date = str(data[1]["date"])
                if temp_date == date:
                    temp_lat = data[1]["lat"]
                    temp_long = data[1]["long"]
                    # tweet_lat, tweet_long = tweet["coordinates"]["coordinates"]
                    distance = np.sqrt((temp_lat-tweet_lat)**2 + (temp_long-tweet_long)**2)
                    temp = data[1]["temp"]
                    # name = data[1]["location"]
                    if distance < min_dist:
                        best_temp = temp
                        # best_name = name
                        min_dist = distance
            d = {}
            d['temp'] = best_temp
            d['sentiment'] = tweet['sentiment']

            str_dict = str(d)
            str_dict += '\n'
            # add a newline to make it a file where dicts are lines

            yield None, str_dict

    # def reducer_init(self):
    #     self.regression_data = {}

    def reducer(self, temp, sentiment):
        
        


            # tweet["sentiment"]


            # tweet_lat, tweet_long = tweet["coordinates"]["coordinates"]

            # yield lat, date
        # yield date
            # yield row["sentiment"], type(row)
        # for data in self.temp_data.iterrows():
        #     temp_date = data[1]["date"]
        #     yield rows, type(rows)
            # if temp_date == date:
            #     tweet_latitude = rows
            #     tweet_longitude
            #     yield True, 1
            # yield temp_date, type(temp_date)
            # if data["date"] == date:
            #     yield 1,2 
        # yield self.temp_data, 1
        # yield self.temp_data, 1
        # for i, row in self.temp_data.iterrows():
        #     yield row, i
        #     yield data[2], 1
            # yield data, 1
            # yield min_dist, 1
            # if data[2] == date:
            #     tweet_latitude, tweet_longitude = row["coordinates"]["coordinates"]
            #     yield tweet_latitude, tweet_longitude
            # else:
            #     pass
        #         weather_latitude = data["lat"]
        #         weather_longitude = data["long"]
        #         distance = np.sqrt((weather_latitude-tweet_latitude)^2 - (weather_longitude-tweet_longitude)^2)
        #         if distance < min_dist:
        #             temp = data["temp"]
        #             min_dist = distance
        #         else:
        #             pass
        #     else: 
        #         pass
        # yield temp, 1




    #     yield self.data["date"], date
      # for data in self.data:
        #     yield data[, 1
            # data = json.load(temperature_data)
            # if date == data["date"]:
            #     yield 3, 1

	        # store = []
	        # yield len(row), 1
	        # if len(row) == 8:
            # tweet_latitude, tweet_longitude = row["coordinates"]["coordinates"]
            # sentiment = row["sentiment"]
            # store.extend((tweet_latitude, tweet_longitude, sentiment))
            # date = row["created_at"]
            # month = date[4:7]
            # month_num = month_dictionary[month] 
            # date = date[-4:] + month_num + date[8:10]
            # yield date, row
	        # else: 
	        #     date = row["date"]
	        #     weather_latitude = row["latitude"]
	        #     weather_longitude = row["longitude"]
	        #     temperature = row["average_temp"]
	        #     location = row["location"]
	        #     store.extend((weather_latitude, weather_longitude, temperature, location))
	        
	        # yield date, store

	    # def combiner(self, date, values):
	    #     data1 = []
	    #     data2 = []
	    #     value = list(values)
	    #     for data in value:
	    #         if len(data) == 3:
	    #             data1.append(data)
	    #         else:
	    #             data2.append(data)

	    #     yield len(data1), len(data2)

        	# if len(tweet) == 0:
        	# 	pass
	        # min_dist = 10000000
	        # for weather in data2:
	        #     distance = np.sqrt((tweet[0]-weather[0])^2 - (tweet[1]-weather[1])^2)
	        #     yield distance, 1
	        #     if distance < min_dist:
	        #         min_dist = distance
	        #         temp = weather[2]
	        #     else:
	        #         pass  
	        # yield temp, tweet[2]


        # for data1 in value:
        #     if len(data1) == 3:
        #         min_dist = 10000000
        #         # yield data1[2], data1[3]
        #         for x in list(values):
        #         	yield x, 1
                    # if len(data2) == 4:
                    # 	yield data1[1], 2
                #     	yield data2[3], data1[0]
            #             distance = np.sqrt((data1[0]-data2[0])^2 - (data1[1]-data2[1])^2)
            #             if distance < min_dist:
            #                 min_dist = distance
            #                 temp = data2[2]
            #         else:
            #         	pass
            #     yield temp, data1[2]
            # else:
            # 	pass


                     # if len(data2) == 4:
                    #     yield data1, data2
                    # else:
                    #     yield 1, 2


        #         for info in values
        #         if len(data == 4):

        # yield list(values)
        # if len(list(values)) == 3:
        #     for data in values:
        #         lat1 = 
        #     lat1 = tweet_latitude[0]
        #     lat2 = tweet
        # else:
        #     lat3 = 
        # for i in list(values):
        #     yield i, 2
           # tweet_latitude, tweet_longitude = row["coordinates"]["coordinates"]
            # sentiment = row["sentiment"]
            # yield sentiment, 1


    # def reducer(self, date, values):
    #     for i in values:
    #         yield i, 1
        # for i in row:
        #     yield i, 1
        # if len(row) == 8:
        #     tweet_latitude, tweet_longitude = row["coordinates"]["coordinates"]
        #     sentiment = row["sentiment"]
        #     yield sentiment, 1

if __name__ == '__main__':
  NearestNeighbor.run()