# CS_123_project
An analysis of the interaction between weather and sentiment using python and hadoop

Specifically, our group is interested in doing and statistical analysis of whether warm weather has a causal impact on Twitter users' sentiment. Out group hypothesizes that temperature has a non-linear relationship with sentiment (i.e. there is a 'perfect' temperature and sentiment peaks). Moreover, we hypothesize that relative changes in temperature are more impactful than absolute temperature (i.e. that 60 degrees in Chicago engenders positive feelings, but 60 degrees in San Diego may not).

To that end, we use mainly a mapreduce framework to parallelize our tasks, which are then run on google cloud compute engines.


Time Series Analysis: Our group wanted to also see the relationship that twitter users had with other twitter uses by comparing each twitter user's timeseries of tweet sentiments with each other users one and see what sort of interesting results we could derive from this. 
Our output from comparing each user's sentiment volatility measure with each other user is found in code/beta_comparison/part-00000. The file shows each user's ID number mapped to a list of users (including themselves) who have similar sentiment volatility measures.

  Files related to time series analysis: time_series.py - helper functions and user beta calculations, MR_time_series.py - map reduce from a twitter json file to map users onto a series of their tweet sentiments over time, MR_Compare_Users.py - map reduce to compare each user's sentiment volatility measure with every other user's sentiment volatility measure, may31/part-00000 - output from MR_time_series.py used as inputs in time_series.py to calculate beta values (sentiment volatility measures).


