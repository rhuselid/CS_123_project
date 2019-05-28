import json
import numpy as np
from mrjob.job import MRJob
from datetime import datetime

class LinearRegression(MRJob):
	# this mapreduce code is written to run a multiple linear regression in parallel 
	# and is intended to be run on a cluster.

    def mapper(self, _, line):
    	line = json.loads(line)
        # read the variables from the line
        # y = line['sentiment'] # psuedo code
		temp = line['temp']
        # season = line['season']
        # season_avg = line['season_avg']
        relative_change = temp - season_avg

        # if type is float then the time is missing
        
        print(type(line))
        print(line['created_at'][0:19])
        # this has to be continued (check if all are formatted the same)
        line['created_at'] = datetime.strptime(line['created_at'][0:19], "%a %b ")
        print(line['created_at'])

        if type(line['created_at'].hour) != float:
            # morning tweet binary variable
            if (line['created_at'].hour <= 3) and (line['created_at'].hour < 12):
                morning = 1
            else:
                morning = 0

            # afternoon tweet binary
            if (line['created_at'].hour >= 12) and (line['created_at'][-7].hour < 18):
                afternoon = 1
            else:
                afternoon = 0

            # evening tweet binary
            if (line['created_at'][-7].hour >= 18) or (line['created_at'].hour < 3):
                evening = 1
            else:
                evening = 0
        else:
            # in the case it is missing these still need values to have a consistant-sized matrix
            morning = 0
            afternoon = 0
            evening = 0

        # number of interactions (this may capture if popular tweets are critical of someone else)
        interactions = 0
        if line['reply_count']:
        	interactions += int(line['reply_count'])

        if line['retweet_count']:
        	interactions += int(line['retweet_count'])

        if line['favorite_count']:
        	interactions += int(line['favorite_count'])

        X = np.array([temp, relative_change, morning, afternoon, evening, interactions])
        Y = np.array([sentiment])
        yield 1, 2

    def reducer(self, x, sentiment):
        yield x, sentiment

    def combiner(self, x, sentiment):
        yield location, list(sentiment)


if __name__ == '__main__':
  LinearRegression.run()