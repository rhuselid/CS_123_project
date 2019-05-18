!sudo pip3 install numpy

from mrjob.job import MRJob
import json
import nltk
import re

#nltk.download('stopwords')
#nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
stop_words=set(stopwords.words("english"))

# help from: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
# and https://opensourceforu.com/2016/12/analysing-sentiments-nltk/

#.mrjob.conf 

# fill out the runners 

# make a compute engine machine--create a VM with the data, then js.util to make a googlecloud storage bucket

# mrjob will allow you to specify the data you want to run (url to data)

# have to turn this into a signle compendium file -- turn to csv or json
# can concat files together with cat command in bash

# should be connecting to the VM with ssh from lab2

# look into nltk to detect language or filter out by 1.0 neutral

# looking for stopwords is more efficient

# 

WORD_RE = re.compile(r"[\w']+")

class AnalyzeSentiment(MRJob):

    def mapper(self, _, line):
        #print(line)
        line = json.loads(line)
        #print(line.keys())
        #time = line['timestamp_ms']
        if ('geo' in line.keys()) and (line['geo']):
            top = 49.3457868 # north lat
            left = -124.7844079 # west long
            right = -66.9513812 # east long
            bottom =  24.7433195 # south lat
            # above continental us borders pulled from: https://gist.github.com/jsundram/1251783

            lat = line['geo']['coordinates'][0]
            lon = line['geo']['coordinates'][1]
            print(lat, lon)
            
            if (bottom < lat and top > lat) and (left < lon and right > lon):
                if 'text' in line.keys():
                    text = line['text']
                    filtered = ''
                    for word in WORD_RE.findall(text):
                        if word not in stop_words:
                            if filtered:
                                filtered += ' '
                            filtered += str(word)
                    print(filtered)
                    sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)#['pos']
                    
                    yield [lat, lon], sentiment


    def combiner(self, location, sentiment):
        yield location, list(sentiment)


    def reducer(self, location, sentiment):
        yield location, list(sentiment)


if __name__ == '__main__':
    AnalyzeSentiment.run()