import json

top = 49.3457868 # north lat
bottom =  24.7433195 # south lat
left = -124.7844079 # west long
right = -66.9513812 # east long

# makes sure that the tweet was from the continental US (which is where our other data 
# source is from). Borders coordinates pulled from: https://gist.github.com/jsundram/1251783

def save_relevant_tweets():
    '''
    This function reads all.json from disk and saves the relevant parts of it 
    (i.e. tweets that are geotagged and in the continental US) into a new file.

    To increase computational efficiency for such a large file,  is a limiting 
    '''
    with open('larger_filtered_tweets.json', 'w') as outfile:
    # creates a new file called filter_tweets.json which will include only the relevant slice

        with open('all.json') as f:
            for l in f:
                line = json.loads(l)

                if ('geo' in line.keys()) and (line['geo']):
                # makes sure it is geotagged

                    lat = line['geo']['coordinates'][0]
                    lon = line['geo']['coordinates'][1]
                        
                    if (bottom < lat and top > lat) and (left < lon and right > lon):
                    # within US boundaries
                        if ('lang' in line.keys()) and (line['lang'] == 'en'):
                        # makes sure that the language is English (analysis is resticted to English only)
                            if 'text' in line.keys():
                            # makes sure there is text content to analyze
                                str_dict = json.dumps(line, outfile)
                                outfile.write(str_dict + '\n')


if __name__ == '__main__':
    save_relevant_tweets()