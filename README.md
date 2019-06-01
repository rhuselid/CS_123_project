# CS_123_project
An analysis of the interaction between weather and sentiment using python and hadoop

Specifically, our group is interested in doing and statistical analysis of whether warm weather has a causal impact on Twitter users' sentiment. Out group hypothesizes that temperature has a non-linear relationship with sentiment (i.e. there is a 'perfect' temperature and sentiment peaks). Moreover, we hypothesize that relative changes in temperature are more impactful than absolute temperature (i.e. that 60 degrees in Chicago engenders positive feelings, but 60 degrees in San Diego may not).

To that end, we use mainly a mapreduce framework to parallelize our tasks, which are then run on google cloud compute engines.
