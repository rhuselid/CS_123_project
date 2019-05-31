import pandas as pd
import json


# with open('sentiment_analyzed.json') as json_data:
#     tweet_data = json.load(json_data)
#     print(tweet_data)
# tweet_data = json.loads("sentiment_analyzed") 
with open('sentiment_analyzed.json') as json_data:
	for line in json_data:
		line = json.loads(line)
		latitude, longitude = line["coordinates"]['coordinates']
# 		sentiment 
# tweet_data = json.dumps(tweet_data)
# print(tweet_data)
# json.load("sentiment_analyzed.json")s

# tweet_data = pd.read_json('sentiment_analyzed.json')
# print(tweet_data)
