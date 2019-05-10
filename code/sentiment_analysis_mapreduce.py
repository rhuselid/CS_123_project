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