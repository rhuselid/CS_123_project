import json
import numpy as np
from mrjob.job import MRJob
from datetime import datetime
from dateutil.parser import parse
import random
import csv

# inspiration on how to approach this project comes from (specifically in the yield structure):
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

        # toy dataset to test the regression output 
        # line = line.split(',')
        # constant, temp, relative_change, morning, afternoon, evening, interactions = int(1 + random.randint(1,101)), int(1 + random.randint(1,101)), int(1 + random.randint(1,101)),int(1 + random.randint(1,101)), int(1 + random.randint(1,101)),int(1 + random.randint(1,101)), int(1 + random.randint(1,101))
        # sentiment = int(1 + random.randint(1,101))

        # print('heres line:')
        # print(line)
        # constant, temp, relative_change, morning, afternoon, evening, interactions = 1, int(line[1]), int(line[2]), int(line[3]), int(line[4]), int(line[5]), int(line[6])
        
        line = json.loads(line)

        # dependent variable (compound sentiment--positive values are positive in sentiment)
        # sentiment = line['sentiment']
        sentiment = random.randint(1,101)


        # independent variables
        constant = 1
        temp = random.randint(1,101)
        season_avg = random.randint(1,101)
        relative_change = temp - season_avg

        # temp = line['temp']
        # season_avg = line['season_avg']
        # relative_change = temp - season_avg

        # if type is float, then the time is missing

        
        # print(type(line['created_at'].hour))

        
        if ('created_at' in line.keys()):
            hour = parse(line['created_at']).hour
            # morning tweet binary variable
            if (hour >= 3) and (hour < 12):
                morning = 1
            else:
                morning = 0

            # afternoon tweet binary
            if (hour >= 12) and (hour < 18):
                afternoon = 1
            else:
                afternoon = 0

            # evening tweet binary
            if (hour >= 18) or (hour < 3):
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
        if 'reply_count' in line.keys():
            interactions += int(line['reply_count'])

        if 'retweet_count' in line.keys():
            interactions += int(line['retweet_count'])

        if 'favorite_count' in line.keys():
            interactions += int(line['favorite_count'])

        X = np.array([constant, temp, relative_change, morning, afternoon, evening, interactions])
        Y = np.array([sentiment])
        # print('heres X AND Y')
        print(X)
        # print(Y)

        x_transpose_x = np.outer(X, X)  # 7 x 7 matrix 
        x_transpose_y = X.T * Y         # 1 x 7 array

        # self.x_transpose_x += np.outer(X, X)
        # self.x_transpose_y += x*y
        # these lines iteratively update these matrices
        # is this thread safe to update a attribute (I don't think so)

        yield None, ('xtx', x_transpose_x.tolist())
        yield None, ('xty', x_transpose_y.tolist())

        #yield 1, list((x_transpose_x.tolist(), x_transpose_y.tolist()))

    def combiner(self, num_obs, values):
        print('reducing')
        sample_size = 0
        x_transpose_x = np.zeros([7,7]) 
        x_transpose_y = np.zeros(7)

        for mat in values:
            sample_size += 1
            
            if mat[0] == 'xty':
                x_transpose_y += np.array(mat[1])
            elif mat[0] == 'xtx':
                x_transpose_x += np.array(mat[1])
            
            # arr_xtx = np.array(mat[0])
            # arr_xty = np.array(mat[1])
            # sample_size += 1
            # x_transpose_x += arr_xtx
            # x_transpose_y += arr_xty

        # print(list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size)))
        # yield 1, list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size))

        yield None, ('xtx', x_transpose_x.tolist())
        yield None, ('xty', x_transpose_y.tolist())
        yield None, ('sample_size', sample_size)
        

    def reducer(self, name, matrices):
        print('combining')
        sample_size = 0
        x_transpose_x = np.zeros([7,7]) 
        x_transpose_y = np.zeros(7)

        for mat in matrices:

            if mat[0] == 'xty':
                x_transpose_y += np.array(mat[1])
            elif mat[0] == 'xtx':
                x_transpose_x += np.array(mat[1])
            else:
                sample_size += mat[1]

        print('xtx', x_transpose_x)
        print('determinate:', np.linalg.det(x_transpose_x))
        print('xty', x_transpose_y)

        # for val in values:
        #     #print(val)
        #     arr_xtx = np.array(val[0])
        #     arr_xty = np.array(val[1])

        #     x_transpose_x += arr_xtx
        #     x_transpose_y += arr_xty
        #     sample_size += val[2]

        # now we need to solve for beta (i.e. the coefficients of the variables)
        # beta = (X′X)−1X′Y

        beta = np.linalg.inv(x_transpose_x) @ x_transpose_y
        #beta = np.linalg.solve(x_transpose_x, x_transpose_y)

        print()
        print('coefficients derived from multiple linear regression')
        print('interpretation: one unit increase in x impact on sentiment')
        print('====================================================')
        print()

        print('intercept                       ', beta[0])
        print('temperature                     ', beta[1])
        print('relative change in temperature  ', beta[2])
        print('tweet was in morning            ', beta[3])
        print('tweet was in afternoon          ', beta[4])
        print('tweet was in evening            ', beta[5])
        print('number of tweet interactions    ', beta[6])

        print()
        print('====================================================')
        print('sample size: ', sample_size)

        # with open('beta_results.csv', 'w') as f:
        #     # row = beta.tolist()
        #     # print(row)
        #     # writer = csv.writer(f)
        #     # writer.writerow(row)
        #     f.write(str(beta))

        # #f.close()

        yield 'beta values: ', beta.tolist()



if __name__ == '__main__':
  LinearRegression.run()