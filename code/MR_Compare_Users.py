from mrjob.job import MRJob


class CompareUsers(MRJob):

    def mapper(self, _, line):


    def combiner(self, location, sentiment):
        yield location, list(sentiment)


    def reducer(self, users, tweets_sentiments):


        yield users, tweets_sentiments


if __name__ == '__main__':
    CompareUsers.run()