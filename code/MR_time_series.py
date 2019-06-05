from mrjob.job import MRJob
import json
# import nltk
import re
import time_series as ts
from datetime import datetime, timedelta
import random
import time

# nltk.download('stopwords')
# nltk.download('vader_lexicon')
# from nltk.corpus import stopwords
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# stop_words=set(stopwords.words("english"))


WORD_RE = re.compile(r"[\w']+")

class TimeSeries(MRJob):

    def mapper(self, _, line):
        '''
        Takes lines from tweet jsons. In our case it was 
        code/sentiment_and_ids.json
        '''

        try:
            line = json.loads(line)

        except Exception as e:
            print("\nInvalid tweet dict found:")
            print(e)
            print("==========================\n")

        else:
            filtered = ''
            
            if ts.is_tweet_of_interest(line):
                user_id = line['user']['id']
                tweet_id = line['id']
                time_stamp = datetime.strptime(line['created_at'], 
                                               '%a %b %d %H:%M:%S %z %Y')
                time_stamp = datetime.timestamp(time_stamp)
                tweet_text = line['text']
                sentiment = line['sentiment']
                lat, lon = line['geo']['coordinates']
                
                '''
                Before, this mapper would also score sentiments but then a 
                teammate decided to filter the corpus of tweets through a
                script and made the sentiment_and_ids.json file which made
                this map reduce much faster and simpler for us. Kept the
                imports in as a comment just to show the code would run
                if we comment the imports back in and this following chunk
                back in as well.
                '''
                # for word in WORD_RE.findall(tweet_text):
                #     if word not in stop_words:
                #         if filtered:
                #             filtered += ' '
                #         filtered += str(word)
                # sentiment = SentimentIntensityAnalyzer()\
                # .polarity_scores(filtered)['compound']

                value_string = "," + str(tweet_id) + ',' + str(sentiment) + \
                               ',' + str(time_stamp) + ',' + str(lat) + ',' +\
                               str(lon)
                
                yield user_id, value_string


    def reducer(self, users, tweets_sentiments):
        '''
        Users: user_ids from users
        tweets_sentiments: sentiments, timestamps, and locations of users
        '''

        ## Eliminate duplicate tweets through making a set
        tweets_sentiments = list(set(tweets_sentiments))

        yield users, str(tweets_sentiments)[2:-2]


if __name__ == '__main__':
    TimeSeries.run()