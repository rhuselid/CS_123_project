from mrjob.job import MRJob

class RunRegression(MRJob):

    def mapper(self, _, line):
    	yield key, val

    def reducer(self, x, sentiment):
        yield location, list(sentiment)

    def combiner(self, x, sentiment):
        yield location, list(sentiment)