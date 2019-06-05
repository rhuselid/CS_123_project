import json
import pandas as pd
from mrjob.job import MRJob
import numpy as np
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
    '''
    This class yields a dictionary of each tweet's associated
    temperature as well as the sentiment of that tweet.
    '''
    def mapper(self, _, line):
        '''
        The mapper designates the key as the date of each tweet and the 
        value as the row or attributes of that tweet(lat, long, sentiment, etc.) 
        '''
        row = json.loads(line)
        date = row["created_at"]
        month = date[4:7]
        month_num = month_dictionary[month] 
        date = date[-4:] + month_num + date[8:10]
        yield date, row

    def combiner_init(self):
        '''
        Initializes the weather data as a pandas dataframe and changes 
        the column names.   
        '''
        self.temp_data = pd.read_csv(r"October_temperature.csv")
        col_names = ["empty1","station_id", "date","temp", "lat", "long", 
        "location", "month"]
        self.temp_data.columns=col_names

    def combiner(self, date, tweets):
        '''
        The combiner iterates over all the tweets in a given day and iterates 
        over the list of stations as well. First,the combiner checks whether
        the station data is on the same day,then it calculates the distance 
        between the tweet and the station. The station with the shortest 
        distance is associated with the tweet and a temperature is established. 
        The combiner yields a dictionary of Null and the values temp, sentiment.
        '''
        best_temp = 0 
        for tweet in tweets:
            min_dist = 1000000
            tweet_lat, tweet_long = tweet["coordinates"]["coordinates"]
            for data in self.temp_data.iterrows():
                temp_date = str(data[1]["date"])
                if temp_date == date:
                    temp_lat = data[1]["lat"]
                    temp_long = data[1]["long"]
                    distance = np.sqrt((temp_lat-tweet_lat)**2 + 
                                        (temp_long-tweet_long)**2)
                    temp = data[1]["temp"]
                    if distance < min_dist:
                        best_temp = temp
                        min_dist = distance
            d = {}
            d['temp'] = best_temp
            d['sentiment'] = tweet['sentiment']

            str_dict = str(d)
            str_dict += '\n'
            # add a newline to make it a file where dicts are lines

            yield None, str_dict

    def reducer(self, _, str_dict):
        '''
        Iterates through string dictionary that was created in the combiner
        yields None and the values in the dictionary to be read into a txt file
        '''
        for line in str_dict:
            yield None, line

if __name__ == '__main__':
  NearestNeighbor.run()
