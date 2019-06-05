from mrjob.job import MRJob
import json


class CompareUsers(MRJob):

    def mapper(self, _, line):
        '''
        Lines are taken from json file of each user mapped to their beta
        value and their locations: code/users_final.json
        '''

        line = json.loads(line)

        user_id = list(line.keys())[0]
        beta = line[user_id]['beta']

        with open("users_final_copy.json") as f:
            for line2 in f:
                line2 = json.loads(line2)

                user_id2 = list(line2.keys())[0]
                beta2 = line2[user_id2]['beta']
                lats2 = line2[user_id2]['lats']
                lons2 = line2[user_id2]['lons']


                if beta != "No beta can be calculated" and \
                   beta2 != "No beta can be calculated":

                    difference = abs(beta - beta2)

                    if difference < 0.05:
                    
                        yield user_id, [user_id2, lats2, lons2]


    def combiner(self, user1_id, similarity_list):
        '''
        user1_id: user_id for person of interest

        similarity_list: iterable. Contains sequence of users that are related
        to user1_id in terms of sentiment volatility (beta)
        '''
        
        similarity_list = list(similarity_list)[0]

        yield user1_id, similarity_list


    def reducer(self, user1_id, similarity_list):
        '''
        user1_id: user_id for person of interest

        similarity_list: iterable. Contains sequence of users that are related
        to user1_id in terms of sentiment volatility (beta)
        '''

        similarity_list = list(similarity_list)[0]

        yield user1_id, similarity_list


if __name__ == '__main__':
    CompareUsers.run()