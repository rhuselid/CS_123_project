import json
import random

# j = json.loads("sentiment_analyzed.json")
tweets = []
for line in open('sentiment_analyzed.json', 'r'):
    tweets.append(json.loads(line))


list_of_random_tweets = random.sample(tweets, 1000)

for tweet in list_of_random_tweets:
	with open("sample_data.json", "w") as f:
		f.write('\n'.join(json.dumps(i) for i in data) + '\n')


# with open('sentiment_analyzed.json') as f:
#     d = json.load(f)
#     print(d)
# 	    print(d)
# # 	f.write('\n'.join(json.dumps(i) for i in data) + '\n')