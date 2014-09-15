import pickle
import userCategory

def main():
    condProbIn  = userCategory.loadConditionalProbInsightful()                                                         
    totalCat = pickle.load(open( 'Data/sortedUsersTotalCategory.p' , 'rb'))
    probUserPostInThread = userCategory.loadThreadProbabilityEachUser();
    totalNumPairs = 0;
    for key in condProbIn:  
        totalNumPairs += 1;
        print "User A and User B: " + str(key)                                                                                          
        print "Conditional Probability " + str(condProbIn[key])
        print "Number of A and B posting in total" + str(totalCat[key])
        #print "Number of B's Post  " + str(totalCat[key[1]]);
        print "Prob B Posting: " + str(probUserPostInThread[key[1]])
        print "Prob A Post Insightful: " + str(condProbIn[(key[0], key[0])])
        print ""

if __name__ == "__main__":
    main();