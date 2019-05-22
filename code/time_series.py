import json
import os
import re
import nltk



users = {}
dict_time_series = {}
jsons_path = "/home/student/CS_123_project/jsons_dir"

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
                        sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)

                        if identification not in dict_time_series:
                            dict_time_series[identification] = []
                        
                        dict_time_series[identification].append(sentiment)



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

    # print("total lines: ", total_line_count)
    # print("total geotags: ", geotag_count)
    # print(geotag_list)


    print(dict_time_series)






