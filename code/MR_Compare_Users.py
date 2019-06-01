from mrjob.job import MRJob
import json


class CompareUsers(MRJob):

    def mapper(self, _, line):

        line = json.loads(line)

        user_id = list(line.keys())[0]
        beta = line[user_id]

        with open("/home/student/CS_123_project/code/all_user_betas_copy.json") as f:
            for line2 in f:
                line2 = json.loads(line2)

                user_id2 = list(line2.keys())[0]
                beta2 = line2[user_id2]


                if beta != "No beta can be calculated" and beta2 != "No beta can be calculated":

                    difference = abs(beta - beta2)

                    if difference < 0.05:
                        print(difference)
                        print("Found small beta")
                    
                        yield user_id, user_id2

                




    # def combiner(self, location, sentiment):
    #     yield location, list(sentiment)


    def reducer(self, user1, similarity_list):

        similarity_list = list(similarity_list)

        yield user1, similarity_list


if __name__ == '__main__':
    CompareUsers.run()