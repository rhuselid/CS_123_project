# CS_123_project
An analysis of the interaction between weather and sentiment using python and hadoop

Specifically, our group is interested in doing and statistical analysis of whether warm weather has a causal impact on Twitter users' sentiment. Out group hypothesizes that temperature has a non-linear relationship with sentiment (i.e. there is a 'perfect' temperature and sentiment peaks). Moreover, we hypothesize that relative changes in temperature are more impactful than absolute temperature (i.e. that 60 degrees in Chicago engenders positive feelings, but 60 degrees in San Diego may not).

To that end, we use mainly a mapreduce framework to parallelize our tasks, which are then run on google cloud compute engines.


Time Series Analysis:
As of June 1 4:09 AM the map reduce job of comparing each user to each other user's sentiment response measure in code/MR_Compare_Users.py is still going on. It has been running for several hours now and we don't know if we can put out the final file before deadline at 10:00 AM June 1. However we have added a sample output from running the script on a much smaller subset of the data (about 300 lines vs 28,000). This can be found in beta_tests/part-00000. The file showseach user's ID number mapped to a list of users (including themselves) who have similar sentiment volatility measures.

  Files related to time series analysis: time_series.py - helper functions and user beta calculations, MR_time_series.py - map reduce from a twitter json file to map users onto a series of their tweet sentiments over time, MR_Compare_Users.py - map reduce to compare each user's sentiment volatility measure with every other user's sentiment volatility measure, may31/part-00000 - output from MR_time_series.py used as inputs in time_series.py to calculate beta values (sentiment volatility measures).


