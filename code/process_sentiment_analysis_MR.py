# this file is intended to process the output of sentiment_analysis_mapreduce.py into a new file
# is it intended to be run locally (the bulk of the work has already been done: sentiment analysis)

from ast import literal_eval

def create_new_json():
	'''
	This function takes in the file created by sentiment_analysis_mapreduce.py 
	and processes that into a new file (intended to be run on a single machine)
	'''

	filename = 'test_output.txt'
	# this is the name of the file we outputted from the mapreduce job

	output_filename = 'sentiment_processed_MR.json'

	with open(output_filename, 'w') as outfile:
		with open(filename) as f:
			for l in f:
				str_dict = str(l[5:])
				# this cuts off the null

				try:
					# try line since occasionally tweets with certian types of emoji's cannot be
					# hashed, which throws an error. This appears to be a small subset of all tweets
					# so it would not matter for data size in a big data context
					line = literal_eval(str_dict)
					outfile.write(line)
				except:
					pass


if __name__ == '__main__':
    create_new_json()
