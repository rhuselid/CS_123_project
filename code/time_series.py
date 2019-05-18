import json



def user_time_series():

	with open("30.json") as test_json:
		line = test_json.readlines()
		line = json.loads(line[0])

		for item in line:
			if item == 'user':
				# print("in user key")
				# print(line[item])
				for item2 in line[item]:
					print('{} : {} \n'.format(item2, line[item][item2]))
					identification = line[item]['id']
					user_location = line[item]['location']
					statuses_count = line[item]['statuses_count']
					followers_count = line[item]['followers_count']
					favorites_count = line[item]['favourites_count']


			# print('\n')
			# print(line.keys())
	print('\nseeing if user items are stored correctly\n')
	print(identification, user_location, statuses_count, followers_count, favorites_count)

