# this file is intended to process the output of sentiment_analysis_mapreduce.py into a new file
# is it intended to be run locally (the bulk of the work has already been done: sentiment analysis)

from ast import literal_eval

def create_new_json():
	filename = 'test_output.txt'
	# this is the name of the file we outputted from the mapreduce job

	output_filename = 'sentiment_processed_MR.json'

	with open(output_filename, 'w') as outfile:
		with open(filename) as f:
			for l in f:
				str_dict = str(l[5:])
				# this cuts off the null

				try:
					line = literal_eval(str_dict)
					outfile.write(line)
				except:
					pass



if __name__ == '__main__':
    create_new_json()
