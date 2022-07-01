# Sometimes it takes too long for the communication to start,
# I am not sure why this happens. It has to do with the mic input.
# 

# I could also do it with the socket module.
# I did not add extra threads for handling the requests.
# The docs explicitly specify that only another thread
# may stop the server, if the server has started with server_forever(). 
# To overcome an 'OSError: [Errno 98] Address already in use' between
# consecutive stop/run of the socket I set the allow_reuse_address to True,
# but it seems that this does not have any effect sometimes.
# 

# TODOs that I do not have the time todo.
# TODO: improve the random generator. Some questions are more 'preferred'
# than others. Maybe hold a list with already proposed questions?
# 
#   review answer as a list and actualAnswer.
#   allow client to shutdown the server with 'exit', etc words.
#   stop using forever and use something else. 
# 

import socketserver
import random
import os # to check whether the questions-answer db exists

# If the question asked was not found this string is the first half
# of the answer. The other second half will be a question from the db.
answerBase = "Try saying: "

# used to check for existing db file with questions and answers
def fileExists(filename):
    return os.path.exists(filename) and os.path.isfile(filename)

class MyTCPHandler(socketserver.BaseRequestHandler):
    
    def handle(self):

        # receive the question in bytes
        self.data = self.request.recv(1024).strip()

        # convert the question from bytes to string
        question = self.data.decode("utf-8").strip()

        # if the question does not have a trailing '?' character, append one.
        # probably not needed, I used this piece of code when I was 
        # typing instead of speaking.
        if question[-1] != '?':
            question += '?'
        
        # will contain alexis' answer. It might have 2 forms.
        # If an answer is found, then it will only contain the answer.
        # If not, we implement a proposal system below. The proposed 
        # answer format is: [answerBase, proposed_question].
        answer = []

        # todo: remove this, do the checks only with the answer var
        # flag to determine whether we have found a matching question in the db.
        actualAnswer=''

        # todo: I did not test that yet 
        if not fileExists("questions_answers_db"):
            answer = "Sorry, the database is missing. You need to restore it."
            self.request.sendall(bytes(answer + '\n', "utf-8"))
            print("missing db. Ctrl+C to stop the program. Restore the db before running.")
            return

        # search through the questions_answers_db file for the question.
        print(f"Examining: {question}")
        with open("questions_answers_db", "r") as handler:

            lines = handler.readlines()

            # used to match the max number of common words between the question
            # asked and any of the questions in the db.
            maxSameWords = 0

            # for each question in the database:
            for idx,line in enumerate(lines):

                # the question that is being examined from the db
                # remove any extra spaces at start and end of the question.
                runningQuestion = line.split(":")[0].strip()
                
                # easy case where we found a matching question. Set the answer.
                if runningQuestion == question:

                    # empties the answer that may have been constructed so far.
                    for i in range(len(answer)):
                        answer.pop()
                    answer.append(line.split(":")[1].strip())
                    actualAnswer = answer[0]
                    print("Found matching question. Answer is: " + answer[0])
                    break

                # count matching words of question asked and the 
                # runningQuestion of db
                sameWords = 0
                for word in runningQuestion.split():
                    for questionWord in question.split():
                        if word == questionWord:
                            sameWords += 1

                # Try hard to find a question to propose.
                if sameWords > 0:

                    # Found a (better) match.
                    if sameWords > maxSameWords:
                        maxSameWords = sameWords

                        # remove any previous propose questions.
                        if len(answer) == 1:
                            answer.pop()

                        # and set the new propose question to the runningQuestion.
                        answer.append(runningQuestion)

                    # We have a tie. It is resolved randomly.
                    # It is extremely important to check for this tie.
                    # To understand why, consider the case where the question asked
                    # is "are you crazy". If not for this check below, the proposed
                    # question (based on the db file) will always be the 4th question.
                    elif sameWords == maxSameWords:
                        pickAtRandom = random.randint(0,1)
                        if pickAtRandom == 0:
                            print(f"random number (0,1): {pickAtRandom} so we will replace {answer[0]} with {runningQuestion}")
                            if len(answer) == 1:
                                answer.pop()
                            answer.append(runningQuestion)
                        else:
                            print(f"random number (0,1): {pickAtRandom} so no replacement took place")


        # if we did not find a matching question, then generate an
        # answer. The answer will be the answerBase string + a random
        # question from the questions db
        if len(answer)==0:
            print("The question asked was not found.")
            print("Furthermore, all words of the question are not the same\nwith any of the words of the questions in our db.")
            print("Generating totally random question to be proposed...")
            hintQuestion = lines[(random.randint(0, len(lines)-1))].split(":")[0].strip()
            answer = answerBase + hintQuestion

        # we found an exact match of the question and have an actual answer!
        elif len(answer)==1 and actualAnswer!='':
            print("Found a match!")
            print(f"The question was: \"{question}\" and the answer is \"{answer[0]}\"")
            answer = answer[0]

        # we did not find a match, but we found some common words
        else:
            print("Did not find a match, but found some proposals!")
            print(f"The question asked was \"{question}\" and the proposal question is \"{answer[0]}\"")
            answer.insert(0, answerBase)
            answer = answer[0] + answer[1]

        self.request.sendall(bytes(answer + '\n', "utf-8"))
        print("\nSometimes, it might seem that the server takes too long.")
        print("It is probably your client voice recognition that has the problem")
        

if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 65000
    print("Sometimes, it might seem that the server takes too long.")
    print("It is probably the client voice recognition that has the problem")
    print("Read the comment section of client.py on how to use text input instead of mic.")
    print("If you get OSError [Errno 98] you need to wait a bit.\n")
    
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        try: 
            server.serve_forever()
            server.allow_reuse_address = True
        
        # the docs state that we need another thread to 
        # kill the server. Nevertheless, I left this piece of 
        # code here.
        except KeyboardInterrupt as e:
            print("Bye")
            server.shutdown()
