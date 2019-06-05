import json
import pandas as pd
from mrjob.job import MRJob
import numpy as np
import datetime

import csv

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

    def reducer_init(self):
        '''
 
        '''
        # self.temperature_data = json.loads(temperature)

        self.temp_data = pd.read_csv(r"October_temperature.csv")
        col_names = ["empty1","station_id", "date","temp", "lat", "long", "location", "month"]
        self.temp_data.columns=col_names

    def reducer(self, date, tweets):
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

if __name__ == '__main__':
  NearestNeighbor.run()