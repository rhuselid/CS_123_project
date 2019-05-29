import json
import numpy as np
import linalg as 
from mrjob.job import MRJob
from datetime import datetime

# inspiration on how to approach this project comes from:
# https://github.com/AmazaspShumik/MapReduce-Machine-Learning/
#        blob/master/Linear%20Regression%20MapReduce/LinearRegressionTS.py

class LinearRegression(MRJob):
    # this mapreduce code is written to run a multiple linear regression in parallel 
    # and is intended to be run on a cluster.

    # def __init__(self):
    #     # this initialization draws from comes from the above link 
    #     self.n = 0
    #     self.x_transpose_y = np.zeros(6)
    #     self.x_transpose_x = np.zeros([6,6]) 
    #     # creates a 6x6 empty matrix to update
        
    def mapper(self, _, line):
        line = json.loads(line)

        # dependent variable
        sentiment = line['sentiment'] # psuedo code

        # independent variables
        constant = 1
        temp = line['temp']
        season_avg = line['season_avg']
        relative_change = temp - season_avg

        # if type is float, then the time is missing
        
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

        X = np.array([constant, temp, relative_change, morning, afternoon, evening, interactions])
        Y = np.array([sentiment])

        x_transpose_x = np.outer(X, X)  # 7 x 7 matrix 
        x_transpose_y = X*Y             # 1 x 7 array

        # self.x_transpose_x += np.outer(X, X)
        # self.x_transpose_y += x*y
        # these lines iteratively update these matrices
        # is this thread safe to update a attribute (I don't think so)

        yield 1, list(x_transpose_x, x_transpose_y)


    def reducer(self, _, matrices):
        sample_size = 0
        x_transpose_x = np.zeros([7,7]) 
        x_transpose_y = np.zeros(7)

        for mat in matrices:
            sample_size += 1
            x_transpose_x += mat[0] 
            x_transpose_y += mat[1]

        yield 1, list(x_transpose_x, x_transpose_y, sample_size)


    def combiner(self, num_obs, values):
        sample_size = 0
        x_transpose_x = np.zeros([7,7]) 
        x_transpose_y = np.zeros(7)

        for val in values
            x_transpose_x += values[0] 
            x_transpose_y += values[1]
            sample_size += values[2]

        # now we need to solve for beta (i.e. the coefficients of the variables)
        # beta = (X′X)−1X′Y

        beta = np.linalg.inv(x_transpose_x) @ x_transpose_y

        print()
        print('coefficients derived from multiple linear regression')
        print('====================================================')
        print()

        print('intercept:                      ', beta[0])
        print('temperature                     ', beta[1])
        print('relative change in temperature  ', beta[2])
        print('tweet was in morning            ', beta[3])
        print('tweet was in afternoon          ', beta[4])
        print('tweet was in evening            ', beta[5])
        print('number of tweet interactions    ', beta[6])

        print()
        print('====================================================')

        yield 'hurray it worked!', betas

if __name__ == '__main__':
  LinearRegression.run()