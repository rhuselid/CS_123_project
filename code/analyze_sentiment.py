from mrjob.job import MRJob
import json
import nltk
import re

nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words=set(stopwords.words("english"))

WORD_RE = re.compile(r"[\w']+")

# this file is functionally the same as the mapreduce version, but this does not rely on mapreduce.
# (this file was created to deal with analyzing the sentiment on a relatively small json file)

def add_sentiment_key():

    with open('sentiment_analyzed.json', 'w') as outfile:
        complete = []
        with open('30.json') as file:
            for l in file: 
                line = json.loads(l)
                if 'text' in line.keys():
                    relevant = {}

                    text = line['text']
                    filtered = ''
                    for word in WORD_RE.findall(text):
                        if word not in stop_words:
                            # not including stop words helps to reduce the noise

                            if filtered:
                                filtered += ' '
                            filtered += str(word)

                    sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)

                    # another way to go about this process (reduces the disk impact by culling the relevant data)
                    relevant['sentiment'] = sentiment['compound']

                    try:
                        relevant['reply_count'] = line['reply_count']
                    except:
                        print('no replies')
                    try:
                        relevant['retweet_count'] = line['retweet_count']
                    except:
                        print('no retweets')
                    try: 
                        relevant['favorite_count'] = line['favorite_count']
                    except:
                        print('no favorites')                    
                    try:
                        relevant['coordinates'] = line['coordinates']
                    except:
                        print('no coordinates')
                    try:
                        relevant['created_at'] = line['created_at']
                    except:
                        print('no date')
                    try:
                        relevant['geo'] = line['geo']
                    except:
                        print('no geotag')
                    try:
                        relevant['lang'] = line['lang']
                    except:
                        print('no language')

                    # adds a new key, val to the json
                    complete.append(relevant)
            json.dump(complete, outfile)
        file.close()
    outfile.close()

    return complete


if __name__ == '__main__':
    add_sentiment_key()