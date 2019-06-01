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

        try:
            line = json.loads(line)

        except Exception as e:
            print("\nWe have an exception here it is:")
            print(e)
            print(len(line))
            print("==========================\n")

        else:
            print("Got past the exception\n")
            filtered = ''
            
            if ts.is_tweet_of_interest(line):
                user_id = line['user']['id']
                tweet_id = line['id']
                time_stamp = datetime.strptime(line['created_at'], 
                                               '%a %b %d %H:%M:%S %z %Y')
                time_stamp = datetime.timestamp(time_stamp)
                tweet_text = line['text']
                sentiment = line['sentiment']
                
                '''
                Before, this mapper would also score sentiments but then a 
                teammate decided to filter the corpus of tweets through a
                script and made the sentiment_and_ids.json file which made
                this map reduce much faster and simpler for us.
                '''
                # for word in WORD_RE.findall(tweet_text):
                #     if word not in stop_words:
                #         if filtered:
                #             filtered += ' '
                #         filtered += str(word)
                # sentiment = SentimentIntensityAnalyzer()\
                # .polarity_scores(filtered)['compound']

                value_string = "," + str(tweet_id) + ',' + str(sentiment) + \
                               ',' + str(time_stamp)
                
                yield user_id, value_string


    def reducer(self, users, tweets_sentiments):

        ## Eliminate duplicate tweets through making a set
        tweets_sentiments = list(set(tweets_sentiments))

        yield users, str(tweets_sentiments)[2:-2]


if __name__ == '__main__':
    TimeSeries.run()