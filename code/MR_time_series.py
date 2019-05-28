from mrjob.job import MRJob
import json
import nltk
import re
import time_series as ts
from datetime import datetime, timedelta

nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words=set(stopwords.words("english"))


WORD_RE = re.compile(r"[\w']+")

class TimeSeries(MRJob):

    def mapper(self, _, line):
        line = json.loads(line)
        filtered = ''
        
        if ts.is_tweet_of_interest(line):
            user_id = line['user']['id']
            tweet_id = line['id']
            time_stamp = datetime.strptime(line['created_at'], '%a %b %d %H:%M:%S %z %Y')
            time_stamp = datetime.timestamp(time_stamp)
            tweet_text = line['text']
            
            for word in WORD_RE.findall(tweet_text):
                if word not in stop_words:
                    if filtered:
                        filtered += ' '
                    filtered += str(word)
            sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)['compound']
            
            yield user_id, (tweet_id, sentiment)


    # def combiner(self, location, sentiment):
 #        yield location, list(sentiment)


    def reducer(self, users, tweets_sentiments):

        ## No repeats
        set_tweets_sentiments = set(tweets_sentiments)

        sentiments = [x[1] for x in set_tweets_sentiments]

        ## STILL HAVE TO ADD THE TIME TO EACH SENTIMENT

        yield users, sentiments


if __name__ == '__main__':
    TimeSeries.run()