import json
import os
import re
import nltk
import csv
import datetime



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

                    time_stamp = line['created_at']
                    place = line['place']
                    tweet_id = line['id']
                    tweet_text = line['text']

                    geo = line['geo']
                    if line['geo'] != None:
                        # write_to_json("repeat_tweets.json", {identification: tweet_text})
                        write_csv([tweet_text, tweet_id], "repeat_tweets.csv")
                        geotag_count += 1
                        geotag_list.append(line['geo'])

                        ## Sentiment Analysis for non empty geos (not the USA)
                        filtered = ''
                        for word in WORD_RE.findall(tweet_text):
                            if word not in stop_words:
                                if filtered:
                                    filtered += ' '
                                filtered += str(word)
                        # print(filtered)
                        sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)['compound']
                        # if identification == 889963667520925698 or identification == "889963667520925698":
                        #     print("random user filtered val: ")
                        #     print(filtered)
                        if identification not in dict_time_series:
                            dict_time_series[identification] = [[],[],[]]
                        
                        dict_time_series[identification][0].append(sentiment)
                        dict_time_series[identification][1].append(filtered)
                        dict_time_series[identification][2].append(time_stamp)



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
        print(useri,":", dict_time_series[useri][2])
        print("\n")



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

    d = datetime.strptime(test, '%a %b %d %H:%M:%S %z %Y')

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











