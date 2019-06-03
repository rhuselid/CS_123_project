import json
import numpy as np
from mrjob.job import MRJob
import random
# from datetime import datetime
# from dateutil.parser import parse

# inspiration on how to approach mapreduce linear regression comes from (specifically in the yield structure + updating matrices):
# https://github.com/AmazaspShumik/MapReduce-Machine-Learning/blob/master/Linear%20Regression%20MapReduce/LinearRegressionTS.py

class LinearRegression(MRJob):
    # this mapreduce code is written to run a multiple linear regression in parallel 
    # and is intended to be run on a cluster.
        
    def mapper(self, _, l):

        # print(l)
        line = json.loads(l)
        # print(line)

        # dependent variable (compound sentiment--positive values are positive in sentiment)
        sentiment = line['sentiment']
        # # sentiment = random.randint(1,1000)

        # # independent variables
        constant = 1

        # # these lines are fake inputs for testing purposes until the twitter-weather merge is complete
        temp = random.randint(1,1000)
        season_avg = random.randint(1,1000)
        relative_change = temp - season_avg

        # temp = line['temp']
        # season_avg = line['season_avg']
        # relative_change = temp - season_avg

        ############################################################################
        # NOTE: we created a number of control variables (commented out below), but# 
        #       they threw off regression results since they lacked significant    #
        #       variation between the tweets (kept to see thought process and      #
        #       datetime parsing)                                                  #
        ############################################################################


        # if ('created_at' in line.keys()):
        #     hour = parse(line['created_at']).hour
        #     # morning tweet binary variable
        #     if (hour >= 3) and (hour < 12):
        #         morning = 1
        #     else:
        #         morning = 0

        #     # afternoon tweet binary
        #     if (hour >= 12) and (hour < 18):
        #         afternoon = 1
        #     else:
        #         afternoon = 0

        #     # evening tweet binary
        #     if (hour >= 18) or (hour < 3):
        #         evening = 1
        #     else:
        #         evening = 0
        # else:
        #     # in the case it is missing these still need values to have a consistant-sized matrix
        #     morning = 0
        #     afternoon = 0
        #     evening = 0

        # our file had mostly unpopular tweets so there wasn't enough variance here for this to be predicitive
        # number of interactions (this may capture if popular tweets are critical of someone else)
        # interactions = 0
        # if 'reply_count' in line.keys():
        #     interactions += int(line['reply_count'])

        # if 'retweet_count' in line.keys():
        #     interactions += int(line['retweet_count'])

        # if 'favorite_count' in line.keys():
        #     interactions += int(line['favorite_count'])

        X = np.array([constant, temp, relative_change])
        Y = np.array([sentiment])

        x_transpose_x = np.outer(X, X)  # 3 x 3 matrix 
        x_transpose_y = X.T * Y         # 1 x 3 array

        yield None, ('xtx', x_transpose_x.tolist())
        yield None, ('xty', x_transpose_y.tolist())

        # yield None, list(line) 

    def combiner(self, num_obs, matrices):
        # print('reducing')
        sample_size = 0
        x_transpose_x = np.zeros([3,3]) 
        x_transpose_y = np.zeros(3)

        for mat in matrices:
            sample_size += 1
            
            if mat[0] == 'xty':
                x_transpose_y += np.array(mat[1])
            elif mat[0] == 'xtx':
                x_transpose_x += np.array(mat[1])
            
        # # print(list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size)))
        # # yield 1, list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size))

        yield None, ('xtx', x_transpose_x.tolist())
        yield None, ('xty', x_transpose_y.tolist())
        yield None, ('sample_size', sample_size)

        # yield num_obs, list(matrices)
        

    def reducer(self, name, matrices):
        # print('combining')
        sample_size = 0
        x_transpose_x = np.zeros([3,3]) 
        x_transpose_y = np.zeros(3)

        for mat in matrices:

            if mat[0] == 'xty':
                x_transpose_y += np.array(mat[1])
            elif mat[0] == 'xtx':
                x_transpose_x += np.array(mat[1])
            else:
                sample_size += mat[1]

        # # print('xtx', x_transpose_x)
        # # print('determinate:', np.linalg.det(x_transpose_x))
        # # print('xty', x_transpose_y)

        # # now we need to solve for beta (i.e. the coefficients of the variables)
        # # beta = (X′X)−1X′Y
        beta = np.linalg.inv(x_transpose_x) @ x_transpose_y

        # # print()
        # # print('coefficients derived from multiple linear regression')
        # # print('interpretation: one unit increase in x impact on sentiment')
        # # print('====================================================')
        # # print()

        # # print('intercept                       ', beta[0])
        # # print('temperature                     ', beta[1])
        # # print('relative change in temperature  ', beta[2])
        # # print('tweet was in morning            ', beta[3])
        # # print('tweet was in afternoon          ', beta[4])
        # # print('tweet was in evening            ', beta[5])
        # # print('interaction count               ', beta[6])

        # # print()
        # # print('====================================================')
        # # print('sample size: ', sample_size)


        # # writing to file was a poor idea in a mapreduce context

        # # with open('beta_results.csv', 'w') as f:
        # #     # row = beta.tolist()
        # #     # print(row)
        # #     # writer = csv.writer(f)
        # #     # writer.writerow(row)
        # #     f.write(str(beta))

        # # #f.close()

        yield 'beta values: ', beta.tolist()

        # yield name, list(matrices)



if __name__ == '__main__':
  LinearRegression.run()