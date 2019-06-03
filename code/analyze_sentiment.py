import json
import nltk
import re

nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words = set(stopwords.words("english"))

WORD_RE = re.compile(r"[\w']+")

# this file is functionally the same as the mapreduce version of a similar name, but this does 
# file is meant to be run on a single machine.

def add_sentiment_key():

    with open('sentiment_and_ids.json', 'w') as outfile:

        with open('larger_filtered_tweets.json') as file:
            for l in file: 
                line = json.loads(l)

                if 'text' in line.keys():

                    # writing only the relevant keys to output to save on file size
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

                    relevant['sentiment'] = sentiment['compound']

                    try:
                        relevant['text'] = line['text']
                    except:
                        print('no text')
                        relevant['text'] = ''

                    try:
                        relevant['reply_count'] = line['reply_count']
                    except:
                        print('no replies')
                        relevant['reply_count'] = ''

                    try:
                        relevant['retweet_count'] = line['retweet_count']
                    except:
                        print('no retweets')
                        relevant['retweet_count'] = ''

                    try: 
                        relevant['favorite_count'] = line['favorite_count']
                    except:
                        print('no favorites')
                        relevant['favorites'] = ''

                    try:
                        relevant['coordinates'] = line['coordinates']
                    except:
                        print('no coordinates')
                        relevant['coordinates'] = ''

                    try:
                        relevant['created_at'] = line['created_at']
                    except:
                        print('no date')
                        relevant['created_at'] = ''

                    try:
                        relevant['geo'] = line['geo']
                    except:
                        print('no geotag')
                        relevant['geo'] = '' 

                    try:
                        relevant['lang'] = line['lang']
                    except:
                        print('no language')
                        relevant['lang'] = ''

                    try:
                        relevant['id'] = line['id']
                    except:
                        print('no id')
                        relevant['id'] = ''

                    try:
                        relevant['user'] = line['user']
                    except:
                        print('no user')
                        relevant['user'] = ''

                    str_dict = json.dumps(relevant, outfile)
                    outfile.write(str_dict + '\n')
            
            # json.dump(complete, outfile)

        file.close()

    outfile.close()

    # ret = {{str(key): str(val) for key, val in d.items()} for d in complete}
    # print(ret)


if __name__ == '__main__':
    add_sentiment_key()