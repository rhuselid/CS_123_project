import json
import os
import re
import nltk
import csv
from datetime import date, datetime, timedelta

users = {}
dict_time_series = {}
jsons_path = "/home/student/CS_123_project/jsons_dir"
bug_dict = {}

WORD_RE = re.compile(r"[\w']+")

nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words=set(stopwords.words("english"))
## Start / End date for data: 1/1/18 - 10/31/18

north_border = 49.3457868 # north lat
west_border = -124.7844079 # west long
east_border = -66.9513812 # east long
south_border =  24.7433195 # south lat
# above continental us borders pulled from: https://gist.github.com/jsundram/1251783

def create_date_indexer():
    '''
    Create indexer. WIll allow us to map which days to include
    when we compare betas.
    '''
    d = {}
    d_inverse = {}

    start = datetime.strptime("01-06-2018", "%d-%m-%Y")
    end = datetime.strptime("31-10-2018", "%d-%m-%Y")

    for x in range(0,(end-start).days + 1):
        d[start + timedelta(days=x)] = x
        d_inverse[x] = start + timedelta(days=x)

    return d, d_inverse


def is_tweet_of_interest(line):
    '''
    Skip tweet if the tweet given does not meet criteria.
    ##
    line: tweet dictionary already loaded from json

    More elegant way to iterate through files:
    with open('30.json') as test_json:
   ...:     for line in test_json:
   ...:         line = json.loads(line)
   ...:         if 'delete' in line:
   ...:             print(i)
   ...:         i += 1
   ...:         holder2.append(line)
    '''

    if 'delete' in line:
        return False

    # if not line['geo']:
    #     return False

    # lat = line['geo']['coordinates'][0]
    # lon = line['geo']['coordinates'][1]
    # print('im in tweet of interest')

    # if not ((south_border < lat and lat < north_border) and
    #         (west_border < lon and lon < east_border)):
    #     return False

    # print('still here')

    ## How to deal with repeat tweets though?

    return True

def aggregate_sentiment_index(num_users, min_lines, user_time_series_file):

    ## If 3 componenets after user Id: things rotate in mod 4 with offset 1
    ## bcz first element is non repeating user id with an end quote
    ## time stamp always has end quotes...
    temp_count = 0
    num_user_fields = 4 ## including extra comma
    users = {}
    ## might also want to accumulate users randomly

    with open(user_time_series_file) as f:
        for line in f:
            print('line before: ')
            print(line)
            line2 = ''.join(line.split())
            line2 = line2.split(",")

            user_id = int(line2[0][:-1])
            users[user_id] = []
            
            line_length = len(line2)


            for i in range(line_length):
                if i % num_user_fields == 3:
                    users[user_id].append((float(line2[i-1]), float(line2[i][:-1])))



            temp_count += 1

            if temp_count == 10:
                return users



            # time_stamp = int(line[1].split("|")[2][:-4])

            # print("=======================\n")
            # for index, element in enumerate(line2):
            #     print("_____________________")
            #     print("heres element: ", index)
            #     print(element)
            #     print("__________________")
            # # print(line3





def user_time_series():

    total_line_count = 0
    geotag_count = 0
    geotag_list = []
    for filename in os.listdir(jsons_path):
        print(filename)
        file_path = jsons_path + "/" + filename

        with open(file_path) as test_json:
            
            # try:
            lines = test_json.readlines()
            num_lines = len(lines)
            total_line_count += num_lines

            for i in range(num_lines):
                line = json.loads(lines[i])
                # total_line_count += 1
                # for l in lines:
                #   l = json.loads(l)

                #   if 'geo' in l:

                #       if l['geo'] != None:
                #           print('geo : {}'.format(l['geo']))

                for item in line:
                    # print('{} : {} \n'.format(item, line[item]))
                    # print(item)

                    ## We're going to ignore deleted tweets because it has no data
                    if item == 'delete':
                        total_line_count -= 1
                        continue
                    if item == 'user':

                        ## 'users' is another dictionary
                        for item2 in line[item]:
                            # print('{} : {} \n'.format(item2, line[item][item2]))
                            identification = line[item]['id']
                            user_location = line[item]['location']
                            statuses_count = line[item]['statuses_count']
                            followers_count = line[item]['followers_count']
                            favorites_count = line[item]['favourites_count']
                            # print(users)

                        users[identification] = users.get(identification, 0) + 1

                    time_stamp = datetime.strptime(line['created_at'], '%a %b %d %H:%M:%S %z %Y')
                    
                    ## Convert time_stamp to unix so it is comparable with other times
                    time_stamp = datetime.timestamp(time_stamp)

                    place = line['place']
                    tweet_id = line['id']
                    tweet_text = line['text']

                    geo = line['geo']
                    if line['geo'] != None:
                        # write_to_json("repeat_tweets.json", {identification: tweet_text})
                        # write_csv([tweet_text, tweet_id], "repeat_tweets.csv")
                        geotag_count += 1
                        geotag_list.append(line['geo'])

                        ## Sentiment Analysis for non empty geos (not the USA)
                        filtered = ''
                        for word in WORD_RE.findall(tweet_text):
                            if word not in stop_words:
                                if filtered:
                                    filtered += ' '
                                filtered += str(word)
                        sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)['compound']
                        # if identification == 889963667520925698 or identification == "889963667520925698":
                        #     print("random user filtered val: ")
                        #     print(filtered)
                        if identification not in dict_time_series:
                            dict_time_series[identification] = [[],[]]
                        
                        # dict_time_series[identification][0].append(sentiment)
                        dict_time_series[identification][0].append((sentiment, time_stamp))
                        dict_time_series[identification][1].append(filtered)
                        # dict_time_series[identification][2].append(time_stamp)



                    '''
                    DO USER SENTIMENT analysis
                    Compare geography?
                    // can do a lat long shape to google map to visualize where we are
                    // have to do in US

                    make time series

                    
                    '''

            # except Exception as e:
            #     print('here is excepton:')
            #     print(e)
            #     print('\n')
            #     print("file name is" + filename)
            #     print('here is the json line:\n')
            #     print(line)
    # print(users)
    # print('\n')

    # for user in users:
    #     if users[user] > 2:
    #         print(user, users[user])

    print("total lines: ", total_line_count)
    print("total geotags: ", geotag_count)
    # print(geotag_list)


    # print(dict_time_series.keys())
    print('users comparison\n')
    print(len(dict_time_series))
    print(len(users))
    print("\n")
    res = 0
    for useri in dict_time_series:
        print(useri,":", dict_time_series[useri][0])
        print("\n")
    return dict_time_series



def write_to_json(filename, data):
    with open(filename, "a") as json_file:
        json.dump(data, json_file)

def write_csv(given_list, filename):
    '''
    Takes a list and creates a csv line of that list or appends a new line
    to an already existing csv file

    Inputs:
        given_list (list)
        filename (str): file to store csv

    Returns:
        None
    '''
    with open(filename, "a") as outfile:
        writer = csv.writer(outfile, delimiter="|")
        writer.writerow(given_list)


def user_to_user_comovement(user1_sentimentlist, user2_sentimentlist, time_differential):
    '''
    Calculate the covariance or comovement between two given users' 
    tweet sentiments over time. Tweets must be within time_differential time apart.
    '''

    ## Have to make time pairs because covariance needs equal sample size and
    ## if there are more than one data points between users, then the pair 
    
    ## maybe sort the time series? not sure what is the best method for this...
    user1_sentimentlist.sort(key=lambda x: x[1])
    user2_sentimentlist.sort(key=lambda x: x[1])
    time_pairs = []
    d = datetime.strptime(test, '%a %b %d %H:%M:%S %z %Y')

    return

def average_all_tweet_time_neighbors(user_sentimentlist, time_differential, t0_index):
    '''
    def average_all_tweet_time_neighbors(user_sentimentlist, time_stamps, time_differential, t0_index):

    Given a chronologicla list of sentiment scores given time stamps (also sorted),
    return the average of all sentiments in the neighborhood.

    SInce the time series is in order and we are assuming sorted sentiment list of tweets,
    only need to check right neighbors while iterating through

    t0_index: index in sortd time list of time of interest

    time differential has to be in seconds?

    need to do: 

    convert all date times to time stamps..

    '''



    # t_right = datetime.timestamp(time_stamps[t0_index]) + time_differential
    t_right = user_sentimentlist[t0_index][1] + time_differential
    print(t_right)
    print("____")
    total_sentiment = 0
    num_neigbors = 0

    for st_index, st_tuple in enumerate(user_sentimentlist[t0_index:]):
        # print(time)
        # time = datetime.timestamp(time)

        if t_right > st_tuple[1]:
            print()
            total_sentiment += st_tuple[0]
            print(total_sentiment)
            num_neigbors += 1
    ## datetime.datetime.fromtimestamp(timestampitem, tz=datetime.timezone.utc)


    return total_sentiment/num_neigbors, num_neigbors

def generate_datetimes(start, end, time_delta):
    return

def create_national_average_sentiment(users):

    return 







def significant_change_in_sentiment(user_sentimentlist):
    '''
    MIght use a function like this to return a significant swing in sentiment.
    NOt sure of the scientific value of such a function though....
    Time intervals are an issue. 
    '''

def extreme_sentiment_bool(list_of_users_sentimentlists, time_frame):
    '''
    Something like this might be interesting to see if any certain day, 
    hour, month had a significant portion of a sample population tweet negatively
    or positively. COUld be cool to back up the concept that people in new york
    at midnight NYE might feel much more elated than people in california at 9pm
    even though its the same time in the world? Maybe people feel worse after national
    tragedies, etc. 

    If there are more than one tweet per time frame, then we average the tweets sentiments.
    Or consider both? idek

    Returns:
        True or false for a significant portion of population feeling extreme sentiment
        in a given time frame (day, month, hour)

    '''

'''
Potential Idea: does day of the week or time affect sentiment? SImple OLS

'''











