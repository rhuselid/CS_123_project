#!/usr/bin/env python
# coding: utf-8

# # Research question: 
# ## How do different areas of the US compare in regards to Twitter Sentiment? Are there particular areas in the US with remarkably high sentiment?
# 
# *Due to constraints mentioned in the READ_ME, I was only able to work with a subset of the data. The following statistics are based on a sample with 44,964 observations (tweets).*
# 
# Methodology: We partition the US into rectangles of the same dimension. We aim to find the average sentiment for each of these areas and compare. Each rectangle is denoted as a two-tuple (a,b). 

# ## Non-MRJob Implementation and analysis

# In[222]:


import json
data = []
with open("sentiment_and_ids.json") as f:
    for line in f:
        data.append(json.loads(line))
locations = [i["coordinates"]["coordinates"] for i in data]
loc_x = [i[0] for i in locations]
loc_y = [i[1] for i in locations]
sentiments = [i["sentiment"] for i in data]
import matplotlib.pyplot as plt
plt.scatter(loc_x, loc_y)


# We observe that the data mostly covers the continental US. It appears that the density of tweets in the sample is greatest along areas near the east coast and is lowest in the midwest. 

# In[239]:


import numpy as np
n = 360 #number of partitions
dy = (-65 - (-125)) / n
dx = (50 - 24) / n 
rectangles = {(i,j) : [-125 + dx * i, -125 + dx * (i+1), 24 + dy * j, 24 + dy * (j+1)] for i in range(n) for j in range(n)}
d = {}
for i,j,k in zip(loc_x, loc_y, sentiments):
    x_ind = int((i + 125) / dx)
    y_ind = int((j - 25) / dy)
    old_avg = (d.get((x_ind, y_ind), (0,0)))[0]
    old_freq = (d.get((x_ind, y_ind), (0,0)))[1]
    new_avg = (old_avg * old_freq + k)/(old_freq + 1)
    d[(x_ind, y_ind)] = (new_avg, old_freq + 1)


# https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram2d.html

# In[240]:


import pandas as pd
tweet_df = pd.DataFrame.from_dict(d, orient = "index", columns = ["Average Sentiment", "Number of Tweets"])
tweet_df.nlargest(5, "Number of Tweets")


# In[232]:


# The number of keys with observations
len(d.keys())


# In[217]:


# The number of keys with less than 5 observations. 
len(tweet_df[tweet_df["Number of Tweets"] < 5])


# We see that 72% of our clusters have less than 5 observations. Increasing the range of each rectangle would remedy this issue, but this incurs some loss of the ability to measure the effect of sentiment due to location. Weather may vary significantly if we make the rectangles larger, which would undermine our ability to measure the effect of sentiment and weather. 
# 
# Feel free to adjust the number of partitions (360) along each axis! 

# ## MRJob Implementation

# In[167]:


import os
import tempfile

tmpdir = tempfile.mkdtemp()
file_one = os.path.join(tmpdir, 'module_one.py')


with open(file_one, 'w+') as fid:
    fid.write("""import module_4""")


# In[168]:


get_ipython().run_cell_magic('file', 'module_one.py', '\nimport module_4')


# In[177]:


file_4 = os.path.join(tmpdir, 'module_4.py')
with open(file_4, 'w+') as fid:
    fid.write("""
    
from mrjob.job import MRJob
import json

n = 360 #number of partitions
dy = (-65 - (-125)) / n
dx = (50 - 24) / n 

class AvgSentiment(MRJob):

    def mapper(self, _, line):
        line = json.loads(line)
        sentiment = line["sentiment"]
        [loc_x, loc_y] = line["coordinates"]["coordinates"]
    
        x_ind = int((loc_x + 125) / dx)
        y_ind = int((loc_y - 25) / dy)
        
        yield (x_ind, y_ind), (sentiment, 1)
        
    def _reducer_combiner(self, square, senti_count):
        avg, count = 0, 0
        for sentiment, _ in senti_count:
            avg = (avg * count + sentiment) / (count + 1)
            count += 1
        return square, (avg, count)

    def combiner(self, square, senti_count):
        yield self._reducer_combiner(square, senti_count)

    def reducer(self, square, senti_count):
        square, (avg, count) = self._reducer_combiner(square, senti_count)
        yield square, (avg, count)

if __name__ == '__main__':
    AvgSentiment.run()

""")


# In[246]:


get_ipython().run_line_magic('run', '$file_4 sentiment_and_ids.json')

