#!/usr/bin/env python
# coding: utf-8

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


