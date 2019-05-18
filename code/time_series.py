import json



def user_time_series():

	with open("30.json") as test_json:
		lines = test_json.readlines()
		line = json.loads(lines[0])
		for l in lines:
			l = json.loads(l)

			if 'geo' in l:

				if l['geo'] != None:
					print('geo : {}'.format(l['geo']))

'''
		for item in line:
			print('{} : {} \n'.format(item, line[item]))

			time_stamp = line['created_at']
			place = line['place']
			tweet_id = line['id']
			tweet_text = line['text']
			geo = line['geo']

			if item == 'user':
				for item2 in line[item]:
					# print('{} : {} \n'.format(item2, line[item][item2]))
					identification = line[item]['id']
					user_location = line[item]['location']
					statuses_count = line[item]['statuses_count']
					followers_count = line[item]['followers_count']
					favorites_count = line[item]['favourites_count']

	print('\nseeing if user items are stored correctly\n')
	print(identification, user_location, statuses_count, followers_count, favorites_count)
	print("tweet text:\n")
	print(tweet_text)
'''



