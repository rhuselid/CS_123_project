from datetime import date, datetime, timedelta, timezone
import json
import numpy as np


## Final: Start / End date for data in dd-mm-yyyy format
START_DATE = "01-10-2018"
END_DATE = "01-11-2018"

def find_date_range(tweet_file):
    '''
    Purpose:
        We had problems with our dataset. At some point we realized we
        couldn't get all of it in time so we kept refining and choosing 
        smaller datasets and filtered our data multiple times. Because of
        that, we made a function that displays all dates found in any tweet
        data set (which was the master data set) and we could then sort and
        see what the date ranges were. This is important for building
        time series data so we understand when to start and stop our
        index of aggregated sentiments over time.

    Inputs:
        tweet_file: json file of tweet dictionaries

    Returns: 
        Dictionary of all unique dates
    '''
    d = {}
    with open(tweet_file) as f:
        for line in f:
            line = json.loads(line)
            timestamp = datetime.strptime(line['created_at'],
                                          '%a %b %d %H:%M:%S %z %Y')
            timestamp = timestamp.replace(hour=0, minute=0, second=0)
            
            if timestamp not in d:
                d[timestamp] = 1
    return d

def create_date_indexer():
    '''
    Purpose:
        Create an indexer for dates and the index of that date in relation to
        the start and end date of our current dataset. A very broad and useful
        helper function.

    Inputs:
        None

    Returns: 
        Two dictionaries containing datetimes and the integer representing
        the index of that date when sorted from START_DATE - END_DATE
    '''
    d = {}
    d_inverse = {}

    start = datetime.strptime(START_DATE, "%d-%m-%Y")
    end = datetime.strptime(END_DATE, "%d-%m-%Y")

    for x in range(0,(end-start).days + 1):
        d[start + timedelta(days=x)] = x
        d_inverse[x] = start + timedelta(days=x)

    return d, d_inverse

def is_tweet_of_interest(line):
    '''
    Purpose:
        Filter function used for any single tweet

    Inputs:
        line: one tweet preloaded from file as a dictionary

    Returns: 
        Boolean if tweet meets our requirements or not

    **** Example of one of the functions that were semi-redundant but still
         useful. The changing nature of our master data set made this almost
         useless since the master file already filtered out bad lines but
         we map reduced with this function and it is still valid so we are 
         leaving it here.
    '''

    if 'delete' in line:
        return False

    # if not line['geo']:
    #     return False

    # lat = line['geo']['coordinates'][0]
    # lon = line['geo']['coordinates'][1]

    # if not ((south_border < lat and lat < north_border) and
    #         (west_border < lon and lon < east_border)):
    #     return False

    return True

def aggregation_helper(user_dictionary):
    '''
    Purpose:
        aggregate_sentiment_index(.,.,.,.) helper function. Take the users
        dictionary constructed inside the helpee function and returns
        a dictionary containing a type of average of many random days' worth
        of sentiments from random users

    Inputs:
        users dictionary constructed inside aggregate_sentiment_index(.,.,.,.)

    Returns: 
        Dictionary containing key, value: date, aggregated/averaged sentiment
    '''
    return_d = {}

    for key in user_dictionary:
        for item in user_dictionary[key]:
            if item[2] not in return_d:
                return_d[item[2]] = [item[0], 1]
            else:
                return_d[item[2]][0] += item[0]
                return_d[item[2]][1] += 1

    ## Dict comprehension to divide the total sentiment by number of entries
    return_d = {key:[return_d[key][0]/return_d[key][1], return_d[key][1]] 
                for key in return_d}
    return_d = {key:return_d[key][0] for key in return_d}
    
    return return_d

def make_all_user_time_series(user_time_series_file):
    '''
    Purpose:
        Construct dictionary from the output file of MR_time_series.py. The
        dictionary represents the time series of sentiments for each date they
        have tweeted.

    Inputs:
        Output file from MR_time_series.py. In our case it was:
        CS_123_project/code/master.txt

    Returns: 
        Dictionary of each user_id as key and with their sentiment scores 
        and date pairing is as a tuple (representing time that sentiment was
        expressed)
    '''    
    num_user_fields = 6 ## Represents number of features included from the
                        ## map reduce output. num_user_fields is currently
                        ## == 6 due to 5 fields being included and a string
                        ## comma that comes with the map reduce output
    users = {}

    with open(user_time_series_file) as f:
        tmp = 0
        for line in f:

            line2 = ''.join(line.split())
            line2 = line2.split(",")

            user_id = int(line2[0][:-1])

            if user_id not in users:
                users[user_id] = []
            
            line_length = len(line2)

            ## Iterate through the line that is now a list split by delimiters

            for i in range(num_user_fields-1, line_length,
                           num_user_fields):
                    
                sentiment_score = float(line2[i-3])
                time_stamp = float(line2[i-2])

                datetime_obj = datetime.fromtimestamp(time_stamp, 
                                                      tz=timezone.utc)
                datetime_obj = datetime_obj.replace(hour=0, minute=0,
                                                    second=0, tzinfo=None)
                string_date = datetime_obj.strftime("%d %b %Y")

                lat = float(line2[i-1])
                lon = float(line2[i][:-1])
                
                ## Add relevant objects to users dictionary
                users[user_id].append((sentiment_score, time_stamp,
                                       string_date, lat, lon))
    return users

def aggregate_sentiment_index(users_per_day, user_time_series_file):
    '''
    Purpose:
        Construct the index that represents an "average" sentiment of people
        in the United States for each date in the current date range.
        This is analogous to the S&P 500 for stocks

    Inputs:
        users_per_day (int): minimum number of users per day who would have
        their sentiment score be apart of the average for that day
        
        user_time_series_file: Output file from MR_time_series.py. 
        In our case it was: CS_123_project/code/master.txt

    Returns: 
        Dictionary of each user_id as key and with their sentiment scores 
        and date pairing is as a tuple (representing time that sentiment was
        expressed)
    '''
    num_user_fields = 6 ## Represents number of features included from the
                        ## map reduce output. num_user_fields is currently
                        ## == 6 due to 5 fields being included and a string
                        ## comma that comes with the map reduce output
    users = {}
    d, d_inverse = create_date_indexer()

    ## Must keep track of which days have been added to the index thus far
    days_accounted_for = {k:users_per_day for k in list(d_inverse.keys())}
    indexdict = {}

    with open(user_time_series_file) as f:
        for line in f:
                
            ## Stopping condition
            if days_accounted_for == {}:
                return_d = aggregation_helper(users)
                return return_d
            
            line2 = ''.join(line.split())
            line2 = line2.split(",")

            user_id = int(line2[0][:-1])
            users[user_id] = []
            
            line_length = len(line2)

            for i in range(num_user_fields-1, line_length,
                           num_user_fields):
                    
                sentiment_score = float(line2[i-3])
                time_stamp = float(line2[i-2])

                datetime_obj = datetime.fromtimestamp(time_stamp, 
                                                      tz=timezone.utc)
                datetime_obj = datetime_obj.replace(hour=0, minute=0,
                                                    second=0,
                                                    tzinfo=None)
                string_date = datetime_obj.strftime("%d %b %Y")

                lat = float(line2[i-1])
                lon = float(line2[i][:-1])

                ## Add relevant objects to users dictionary
                users[user_id].append((sentiment_score, time_stamp,
                                       string_date, lat, lon))

            if d[datetime_obj] not in days_accounted_for:
                continue
            if days_accounted_for[d[datetime_obj]] <= 0:
                del days_accounted_for[d[datetime_obj]]

                continue

            ## Account for each day by subtracting 1 from a
            ## predetermined minimum (chosen through users_per_day input)
            days_accounted_for[d[datetime_obj]] -= 1

def write_user_betas_to_file(users_time_series_file, outfile_name):
    '''
    Purpose:
        Create the file of each user and their beta value (a measure of how
        volatile a person's sentiment is compared to some index) for
        MR_Compare_Users.py to run as an input for map reduce 

    Inputs:
        outfile_name (str): path/name of file to be written
        
        user_time_series_file: Output file from running MR_time_series.py.
        In our case it was: CS_123_project/code/may31/part-00000

    Returns: 
        None
    '''

    ## Choice for constructing index. 2 is arbitrary
    min_users_per_day = 2

    index_dict = aggregate_sentiment_index(min_users_per_day,
                                           users_time_series_file)
    all_users_time_series = make_all_user_time_series(users_time_series_file)
    user_betas = get_all_betas_and_locations(all_users_time_series, index_dict)

    with open(outfile_name, 'w') as f:
        f.write('\n'.join(json.dumps(i) for i in user_betas) + '\n')
    
def get_all_betas_and_locations(users_time_series_dict, index_dict):
    '''
    Purpose:
        Map each user to their beta value and collect it all in a list of
        {user: beta} dictionaries.

    Inputs:
        users_time_series_dict: dictionary representing users and their
            corresponding time series
        
        index_dict: dictionary representing the sentiment index

    Returns: 
        List of dictionaries of form {users: beta}
    '''
    users_beta_and_locations = []

    for user_id in users_time_series_dict:
        beta = calc_beta(users_time_series_dict, user_id, index_dict)
        lats = [x[3] for x in users_time_series_dict[user_id]]
        lons = [x[4] for x in users_time_series_dict[user_id]]
        d = {user_id: {'beta': beta, 'lats': lats, 'lons': lons}} 
        users_beta_and_locations.append(d)

    return users_beta_and_locations

def calc_beta(users_time_series_dict, user_id, index_dict):
    '''
    Purpose:
        Calculate a single user's beta (measure of sentiment volatitlity in
        relation to some index)

    Inputs:
        users_time_series_dict: dictionary representing users and their
            corresponding time series
        user_id: unique identifier of a user
        index_dict: dictionary representing the sentiment index

    Returns: 
        Float value representing the beta measurement
    '''
    user_time_series = users_time_series_dict[user_id]
    user_sentiments, index_sentiments = [], []

    for data_point in user_time_series:
        user_sentiment = data_point[0]
        user_date = data_point[2]
        index_sentiment = index_dict[user_date]

        index_sentiments.append(index_sentiment)
        user_sentiments.append(user_sentiment)
    
    user_sentiments = np.array(user_sentiments)
    index_sentiments = np.array(index_sentiments)

    ## No further calculations needed
    if len(index_sentiments) == 1:
        return "No beta can be calculated"

    mean_user = np.mean(user_sentiments)
    mean_index = np.mean(index_sentiments)

    user_sentiments -= mean_user
    index_sentiments -= mean_index

    cov = np.dot(user_sentiments, index_sentiments)
    var = np.dot(index_sentiments, index_sentiments)
    
    ## No divide by 0
    if var == 0.0:
        return "No beta can be calculated"

    return cov/var

def write_to_json(outfile_name, data):
    '''
    Takes data (probably a dictionary) and writes it to a json file

    Inputs:
        outfile_name (str): path/name of outfile
        data: any json encodable container or python object

    Returns:
        None
    '''
    with open(outfile_name, "w") as json_file:
        json.dump(data, json_file)



'''
#############################################################################


Below are functions that were previously used and consistently modified and
either became useless or irrelevant due to the changing nature of our goal
post and the change in the format / content of our master data set. Note:
from now on in this python file, the 79 character rule is ignored because
this is essentially code scraps only being shown to provide evidence and
context for the changing nature of our goal post and the master data set. We
also believe it's relatively humorous to see atrocious code following
no standards :). 


#############################################################################
'''


# Old draft global vars and imports

# import csv
# import re
# import nltk
# import os
# users = {}
# dict_time_series = {}
# jsons_path = "/home/student/CS_123_project/jsons_dir"

# WORD_RE = re.compile(r"[\w']+")

# nltk.download('stopwords')
# nltk.download('vader_lexicon')
# from nltk.corpus import stopwords
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# stop_words=set(stopwords.words("english"))

# north_border = 49.3457868 # north lat
# west_border = -124.7844079 # west long
# east_border = -66.9513812 # east long
# south_border =  24.7433195 # south lat
# ## Continental us borders from: https://gist.github.com/jsundram/1251783

# def user_time_series():

#     total_line_count = 0
#     geotag_count = 0
#     geotag_list = []
#     for filename in os.listdir(jsons_path):
#         print(filename)
#         file_path = jsons_path + "/" + filename

#         with open(file_path) as test_json:
            
#             # try:
#             lines = test_json.readlines()
#             num_lines = len(lines)
#             total_line_count += num_lines

#             for i in range(num_lines):
#                 line = json.loads(lines[i])
#                 # total_line_count += 1
#                 # for l in lines:
#                 #   l = json.loads(l)

#                 #   if 'geo' in l:

#                 #       if l['geo'] != None:
#                 #           print('geo : {}'.format(l['geo']))

#                 for item in line:
#                     # print('{} : {} \n'.format(item, line[item]))
#                     # print(item)

#                     ## We're going to ignore deleted tweets because it has no data
#                     if item == 'delete':
#                         total_line_count -= 1
#                         continue
#                     if item == 'user':

#                         ## 'users' is another dictionary
#                         for item2 in line[item]:
#                             # print('{} : {} \n'.format(item2, line[item][item2]))
#                             identification = line[item]['id']
#                             user_location = line[item]['location']
#                             statuses_count = line[item]['statuses_count']
#                             followers_count = line[item]['followers_count']
#                             favorites_count = line[item]['favourites_count']
#                             # print(users)

#                         users[identification] = users.get(identification, 0) + 1

#                     time_stamp = datetime.strptime(line['created_at'], '%a %b %d %H:%M:%S %z %Y')
                    
#                     ## Convert time_stamp to unix so it is comparable with other times
#                     time_stamp = datetime.timestamp(time_stamp)

#                     place = line['place']
#                     tweet_id = line['id']
#                     tweet_text = line['text']

#                     geo = line['geo']
#                     if line['geo'] != None:
#                         # write_to_json("repeat_tweets.json", {identification: tweet_text})
#                         # write_csv([tweet_text, tweet_id], "repeat_tweets.csv")
#                         geotag_count += 1
#                         geotag_list.append(line['geo'])

#                         ## Sentiment Analysis for non empty geos (not the USA)
#                         filtered = ''
#                         for word in WORD_RE.findall(tweet_text):
#                             if word not in stop_words:
#                                 if filtered:
#                                     filtered += ' '
#                                 filtered += str(word)
#                         sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)['compound']
#                         # if identification == 889963667520925698 or identification == "889963667520925698":
#                         #     print("random user filtered val: ")
#                         #     print(filtered)
#                         if identification not in dict_time_series:
#                             dict_time_series[identification] = [[],[]]
                        
#                         # dict_time_series[identification][0].append(sentiment)
#                         dict_time_series[identification][0].append((sentiment, time_stamp))
#                         dict_time_series[identification][1].append(filtered)
#                         # dict_time_series[identification][2].append(time_stamp)

#             # except Exception as e:
#             #     print('here is excepton:')
#             #     print(e)
#             #     print('\n')
#             #     print("file name is" + filename)
#             #     print('here is the json line:\n')
#             #     print(line)
#     # print(users)
#     # print('\n')

#     # for user in users:
#     #     if users[user] > 2:
#     #         print(user, users[user])

#     print("total lines: ", total_line_count)
#     print("total geotags: ", geotag_count)
#     # print(geotag_list)


#     # print(dict_time_series.keys())
#     print('users comparison\n')
#     print(len(dict_time_series))
#     print(len(users))
#     print("\n")
#     res = 0
#     for useri in dict_time_series:
#         print(useri,":", dict_time_series[useri][0])
#         print("\n")
#     return dict_time_series



# def write_csv(given_list, filename):
#     '''
#     Takes a list and creates a csv line of that list or appends a new line
#     to an already existing csv file

#     Inputs:
#         given_list (list)
#         filename (str): file to store csv

#     Returns:
#         None
#     '''
#     with open(filename, "a") as outfile:
#         writer = csv.writer(outfile, delimiter="|")
#         writer.writerow(given_list)


# def user_to_user_comovement(user1_sentimentlist, user2_sentimentlist, time_differential):
#     '''
#     Calculate the covariance or comovement between two given users' 
#     tweet sentiments over time. Tweets must be within time_differential time apart.
#     '''

#     ## Have to make time pairs because covariance needs equal sample size and
#     ## if there are more than one data points between users, then the pair 
    
#     ## maybe sort the time series? not sure what is the best method for this...
#     user1_sentimentlist.sort(key=lambda x: x[1])
#     user2_sentimentlist.sort(key=lambda x: x[1])
#     time_pairs = []
#     d = datetime.strptime(test, '%a %b %d %H:%M:%S %z %Y')

#     return

# def average_all_tweet_time_neighbors(user_sentimentlist, time_differential, t0_index):
#     '''
#     def average_all_tweet_time_neighbors(user_sentimentlist, time_stamps, time_differential, t0_index):

#     Given a chronologicla list of sentiment scores given time stamps (also sorted),
#     return the average of all sentiments in the neighborhood.

#     SInce the time series is in order and we are assuming sorted sentiment list of tweets,
#     only need to check right neighbors while iterating through

#     t0_index: index in sortd time list of time of interest

#     time differential has to be in seconds?

#     need to do: 

#     convert all date times to time stamps..

#     '''



#     # t_right = datetime.timestamp(time_stamps[t0_index]) + time_differential
#     t_right = user_sentimentlist[t0_index][1] + time_differential

#     total_sentiment = 0
#     num_neigbors = 0

#     for st_index, st_tuple in enumerate(user_sentimentlist[t0_index:]):

#         if t_right > st_tuple[1]:

#             total_sentiment += st_tuple[0]
#             num_neigbors += 1

#     return total_sentiment/num_neigbors, num_neigbors


# def significant_change_in_sentiment(user_sentimentlist):
#     '''
#     Might use a function like this to return a significant swing in sentiment.
#     Not sure of the scientific value of such a function though....
#     Time intervals are an issue. 
#     '''

# def extreme_sentiment_bool(list_of_users_sentimentlists, time_frame):
#     '''
#     Something like this might be interesting to see if any certain day, 
#     hour, month had a significant portion of a sample population tweet negatively
#     or positively. COUld be cool to back up the concept that people in new york
#     at midnight NYE might feel much more elated than people in california at 9pm
#     even though its the same time in the world? Maybe people feel worse after national
#     tragedies, etc. 

#     If there are more than one tweet per time frame, then we average the tweets sentiments.
#     Or consider both? idek

#     Returns:
#         True or false for a significant portion of population feeling extreme sentiment
#         in a given time frame (day, month, hour)

#     '''