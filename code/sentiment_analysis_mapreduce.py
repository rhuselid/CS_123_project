##################################################################################

# Note: this file is depreciated (i.e. was not used to produce the resulting json)
#       it is fairly similar to the analyze_sentiment.py version of the file except 
#       this is intented to work with mapreduce. While it was not used to produce the 
#       final output it was shown to work with a smaller json file locally

#################################################################################
import os 
os.system('sudo pip3 install nltk')

from mrjob.job import MRJob
import json
import nltk
import re
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from google.oauth2 import service_account

# help from: https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
# and https://opensourceforu.com/2016/12/analysing-sentiments-nltk/

class AnalyzeSentiment(MRJob):
    # the purpose of this code is to take a json and read is to reduce a large dataset of 
    # tweets into information about sentiment and attached to geo-coordinates.

    # we tested efficiency of removing stop words and text alone (with the 30.json file)
    #     removing stop words:   0m38.099s
    #     no removed stop words: 0m36.641s

    # since this did not significantly change the run time, we removed stop words in tweets.

    def __init__(self, *args, **kwargs):
        super(AnalyzeSentiment, self).__init__(*args, **kwargs)
        nltk.download('stopwords')
        nltk.download('vader_lexicon')
        self.stop_words = set(stopwords.words("english"))
        self.get_words = re.compile(r"[\w']+")


    def mapper(self, _, line):
        line = json.loads(line)

        # below filtering already done in when the json was reduced to current size

        # if (line['lang']) and (line['lang'] == 'en'):
        #     # makes sure that the language is English (analysis is resticted to English only)

        #     if ('geo' in line.keys()) and (line['geo']):
        #         top = 49.3457868 # north lat
        #         left = -124.7844079 # west long
        #         right = -66.9513812 # east long
        #         bottom =  24.7433195 # south lat
        #         # makes sure that the tweet was from the continental US (which is where our other data 
        #         # source is from). Borders coordinates pulled from: https://gist.github.com/jsundram/1251783

        #         lat = line['geo']['coordinates'][0]
        #         lon = line['geo']['coordinates'][1]
                
        #         if (bottom < lat and top > lat) and (left < lon and right > lon):

        if 'text' in line.keys():
            text = line['text']
            filtered = ''
            for word in self.get_words.findall(text):
                if word not in self.stop_words:
                    # not including stop words helps to reduce the noise

                    if filtered:
                        filtered += ' '
                    filtered += str(word)

            sentiment = SentimentIntensityAnalyzer().polarity_scores(filtered)

            new_line = line
            new_line['sentiment'] = sentiment['compound']

            str_new_line = str(new_line)
            
            yield None, str_new_line

    # def combiner(self, _, new_lines):
    #     yield None, new_lines

    def reducer(self, _, new_lines):

        for str_line in new_lines:
            str_line += '\n'

            yield None, str_line

        # this output is then piped into a new file and filtered by another file: 

        # creates a new json file that includes this column this was augmented to since 
        # this does not represent good mapreduce practice (so another similar script 
        # was written)

        # with open('data_with_sentiment.json', 'w') as f:
        #     for line in new_lines:
        #         print('added a new line')
        #         print(line)
        #         json.dump(line, f)

        #     print(f)
        # f.close()

        # yield None, None


if __name__ == '__main__':
    AnalyzeSentiment.run()