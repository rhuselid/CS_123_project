# import os
# os.system('sudo pip3 install numpy')
# os.system('sudo pip3 install random')

import json
# import numpy as np
from mrjob.job import MRJob
import random
# from datetime import datetime
# from dateutil.parser import parse

# inspiration on how to approach mapreduce linear regression comes from (specifically in the yield structure):
# https://github.com/AmazaspShumik/MapReduce-Machine-Learning/blob/master/Linear%20Regression%20MapReduce/LinearRegressionTS.py

class LinearRegression(MRJob):
    # Important Note: this file is an MapReduce implimentation of regression 
    #                   with just lists (no numpy). This was necessary because
    #                   of import permission issues running in a cluster.


    # this mapreduce code is written to run a multiple linear regression in parallel 
    # and is intended to be run on a cluster.

    # def __init__(self, *args, **kwargs):
    #     super(LinearRegression, self).__init__(*args, **kwargs)
    #     os.system('sudo -H pip3 install numpy')
    #     import numpy

    def mapper(self, _, l):
        line = json.loads(l)

        # dependent variable (compound sentiment--positive values are positive in senti+ment)
        sentiment = line['sentiment']
        # # sentiment = random.randint(1,1000)

        # # independent variables
        constant = 1

        # # these lines are fake inputs for testing purposes until the twitter-weather merge is complete
        temp = random.randint(1,1000)
        # temp = 1
        # season_avg = 1.5
        # relative_change = temp - season_avg

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

        # X_n = np.array([constant, temp])
        # Y_n = np.array([sentiment])

        X = [constant, temp]

        # compute outer product:
        outer_product = []
        for x1 in X:
            row = []
            for x2 in X:
                row.append(x1*x2)
            outer_product.append(row)

        x_transpose_y = []
        for x3 in X:
            x_transpose_y.append(x3 * sentiment)

        # print('out prod', outer_product, 'np version', np.outer(X_n, X_n))
        # print('xty', x_transpose_y, 'np version', X_n.T * Y_n)
        # print('xty', x_transpose_y)
        # x_transpose_x = np.outer(X, X)  # 3 x 3 matrix
        # x_transpose_y = X.T * Y         # 1 x 3 array

        # yield None, ('xtx', x_transpose_x.tolist())
        # yield None, ('xty', x_transpose_y.tolist())

        yield None, ('xtx', outer_product)
        yield None, ('xty', x_transpose_y)

        # yield None, list(line) 

    def combiner(self, _, matrices):
        # print('reducing')
        sample_size = 0
        # x_transpose_xn = np.zeros([2,2]) 
        # x_transpose_yn = np.zeros(2)
        x_transpose_x = [[0,0], [0,0]]
        x_transpose_y = [0] * 2

        for mat in matrices:
            sample_size += 1
            
            if mat[0] == 'xtx':
                # x_transpose_xn += np.array(mat[1])
                for ir, row in enumerate(mat[1]):
                    for ic, val in enumerate(row):
                        x_transpose_x[ir][ic] += val
            elif mat[0] == 'xty':
                # x_transpose_yn += np.array(mat[1])
                for i, val in enumerate(mat[1]):
                    # print(x_transpose_y)
                    x_transpose_y[i] += val

        # sample_size = 0
        # x_transpose_x = [[0] * 2] * 2
        # x_transpose_y = [0] * 2
        # print(list(matrices))
        # # print('xtx', x_transpose_x)
        # # print('xty', x_transpose_y)

        # for mat in matrices:
        #     sample_size += 1
            
        #     if mat[0] == 'xtx':
        #         for ir, row in enumerate(mat[1]):
        #             print(row)
        #             for ic, val in enumerate(row):
        #                 print(val)
        #                 x_transpose_x[ir][ic] += val
        #     elif mat[0] == 'xty':
        #         for i, val in enumerate(mat[1]):
        #             # print(x_transpose_y)
        #             x_transpose_y[i] += val
        
        # print('list xtx: ', x_transpose_x, 'np version', x_transpose_xn)
        # print('list xty: ', x_transpose_y, 'np version', x_transpose_yn)
        # # print(list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size)))
        # # yield 1, list((x_transpose_x.tolist(), x_transpose_y.tolist(), sample_size))

        # yield None, ('xtx', x_transpose_x.tolist())
        # yield None, ('xty', x_transpose_y.tolist())
        # yield None, ('sample_size', sample_size)


        yield None, ('xtx', x_transpose_x)
        yield None, ('xty', x_transpose_y)
        yield None, ('sample_size', sample_size)
        

    def reducer(self, _, matrices):
        sample_size = 0
        # x_transpose_xn = np.zeros([2,2]) 
        # x_transpose_yn = np.zeros(2)
        x_transpose_x = [[0,0], [0,0]]
        x_transpose_y = [0] * 2

        for mat in matrices:            
            if mat[0] == 'xtx':
                # x_transpose_xn += np.array(mat[1])
                for ir, row in enumerate(mat[1]):
                    for ic, val in enumerate(row):
                        x_transpose_x[ir][ic] += val
            elif mat[0] == 'xty':
                # x_transpose_yn += np.array(mat[1])
                for i, val in enumerate(mat[1]):
                    # print(x_transpose_y)
                    x_transpose_y[i] += val
            else:
                sample_size += mat[1]

        # print('list xtx: ', x_transpose_x, 'np version', x_transpose_xn)
        # print('list xty: ', x_transpose_y, 'np version', x_transpose_yn)

        # sample_size = 0
        # x_transpose_x = [[0,0], [0,0]]
        # x_transpose_y = [0] * 2
        # # print(x_transpose_x)
        # # print(x_transpose_x)
        # print('hi')

        # for mat in matrices:
        #     sample_size += 1
            
        #     if mat[0] == 'xtx':
        #         # print('heres xtx', mat[1])
        #         for ir, row in enumerate(mat[1]):
        #             for ic, val in enumerate(row):
        #                 x_transpose_x[ir][ic] += val
        #     elif mat[0] == 'xty':
        #         # print('heres xty', mat[1])
        #         for i, val in enumerate(mat[1]):
        #             x_transpose_y[i] += val

        inverse = [[0, 0], [0, 0]]
        determinate = (x_transpose_x[0][0] * x_transpose_x[1][1] - x_transpose_x[0][1] * x_transpose_x[1][0])

        unnormalized_inv = [[x_transpose_x[1][1], -1 * x_transpose_x[0][1]], 
                            [-1 * x_transpose_x[1][0], x_transpose_x[0][0]]]

        for ir, row in enumerate(unnormalized_inv):
            for ic, val in enumerate(row):
                inverse[ir][ic] = (1 / determinate) * unnormalized_inv[ir][ic]

        beta = [0, 0]

        for i, l in enumerate(inverse):
            for j, val in enumerate(l):
                beta[i] += inverse[i][j] * x_transpose_y[j]

        yield 'beta vals: ', beta


        # print('combining')
        # sample_size = 0
        # x_transpose_x = np.zeros([3,3]) 
        # x_transpose_y = np.zeros(3)

        # for mat in matrices:

        #     if mat[0] == 'xty':
        #         x_transpose_y += np.array(mat[1])
        #     elif mat[0] == 'xtx':
        #         x_transpose_x += np.array(mat[1])
        #     else:
        #         sample_size += mat[1]

        # # print('xtx', x_transpose_x)
        # # print('determinate:', np.linalg.det(x_transpose_x))
        # # print('xty', x_transpose_y)

        # # now we need to solve for beta (i.e. the coefficients of the variables)
        # # beta = (X′X)−1X′Y
        # beta = np.linalg.inv(x_transpose_x) @ x_transpose_y

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

        # yield 'beta values: ', beta.tolist()

        # yield name, list(matrices)



if __name__ == '__main__':
  LinearRegression.run()