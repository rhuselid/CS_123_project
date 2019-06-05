import json
import random

with open("sentiment_analyzed.json") as f:
	json_list = []
	for line in f:
		line = json.loads(line)
		json_list.append(line)
	list_of_random_tweets = random.sample(json_list, 500)

with open("random_tweets.json", 'w') as f:
    f.write('\n'.join(json.dumps(i) for i in list_of_random_tweets) + '\n')
