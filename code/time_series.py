import json
import os



users = {}
jsons_path = "/home/student/CS_123_project/test_jsons"



def user_time_series():

	for filename in os.listdir(jsons_path):
		print(filename)
		file_path = jsons_path + "/" + filename

		with open(file_path) as test_json:
			
			try:
				lines = test_json.readlines()
				num_lines = len(lines)
				for i in range(num_lines):
					line = json.loads(lines[i])
					# for l in lines:
					# 	l = json.loads(l)

					# 	if 'geo' in l:

					# 		if l['geo'] != None:
					# 			print('geo : {}'.format(l['geo']))

					for item in line:
						# print('{} : {} \n'.format(item, line[item]))
						# print(item)

						## We're going to ignore deleted tweets because it has no data
						if item == 'delete':
							continue

						time_stamp = line['created_at']
						place = line['place']
						tweet_id = line['id']
						tweet_text = line['text']
						geo = line['geo']

						if item == 'user':

							
							## 'users' is another dictionary
							for item2 in line[item]:
								# print('{} : {} \n'.format(item2, line[item][item2]))
								identification = line[item]['id']
								user_location = line[item]['location']
								statuses_count = line[item]['statuses_count']
								followers_count = line[item]['followers_count']
								favorites_count = line[item]['favourites_count']
								# print(users)

							users[identification] = users.get(identification, 0) + 1


					'''
					DO USER SENTIMENT analysis
					Compare geography?

					
					'''

			except Exception as e:
				print('here is excepton:')
				print(e)
				print('\n')
				print("file name is" + filename)
				print('here is the json line:\n')
				print(line)
	# print(users)
	print('\n')

	for user in users:
		if users[user] > 2:
			print(user)






