import pickle
import userCategory
import userCommentLength

def main():
    condProbIns  = userCategory.loadConditionalProbInsightful()                                                         
    userPairFreqAllClass = userCategory.loadUserPairFrequencyAllClass();
    probUserPostInThread = userCategory.loadThreadProbabilityEachUser();
    userPairFreqInsightful = userCategory.loadUserPairCondFreqInsightful();
    totalNumPairs = 0;
    for key in condProbIns:  
        totalNumPairs += 1;
        print "User A and User B: " + str(key)                                                                                          
        #print "Joint Probability: A post insightful while B present" + str(jointProbIns[key])
        print "Conditional Probability A Post Insightful with B Present" + str(condProbIns[key])
        print "Number of A and B posting in total" + str(userPairFreqAllClass[key])
        #print "Number of B's Post  " + str(totalCat[key[1]]);
        print "Prob B Posting in a Thread: " + str(probUserPostInThread[key[1]])
        print "Prob A Post Insightful: " + str(condProbIns[(key[0], key[0])])
        print "The number posts A made: " + str(userPairFreqAllClass[(key[0],key[0])])
        print "The number of insightful posts A made: " + str(userPairFreqInsightful[(key[0], key[0])])
        print ""

def summarizeCondProbMostActive(numActive):
    condProbIns  = userCategory.loadConditionalProbInsightful()                                                         
    userPairFreqAllClass = userCategory.loadUserPairFrequencyAllClass();
    probUserPostInThread = userCategory.loadThreadProbabilityEachUser();
    userPairFreqInsightful = userCategory.loadUserPairCondFreqInsightful();
    numTotalThreads = userCategory.loadTotalThreadNum();
    activeUsers = userCommentLength.loadMostActiveUsers(numActive);
    for ua in activeUsers:
        for ub in activeUsers:
            if ub == ua:
                continue;
            
            if (ua, ub) in condProbIns:
                numThreadsBposted = int(probUserPostInThread[ub]*numTotalThreads);
                numPostsAmade = userPairFreqAllClass[(ua,ua)];
                numPostsAinsight = userPairFreqInsightful[(ua, ua)]
                if (numThreadsBposted >= 80) and (numPostsAmade >= 90) and (numPostsAinsight >= 20): 
                
                
                    print "Users: (" + ua + " , " + ub + ")";
                    print "The number of posts A made:\t\t\t\t\t" + str(numPostsAmade)
                    print "The number of posts B made:\t\t\t\t\t" + str(userPairFreqAllClass[(ub,ub)])
                    print "Number of threads B posted:\t\t\t\t\t" + str(numThreadsBposted)
                    print "The number of insightful posts A made:\t\t\t\t" + str(numPostsAinsight)
                    print "Prob A Post Insightful:\t\t\t\t\t\t" + str(condProbIns[(ua, ua)])
                    print "Conditional Probability A Post Insightful with B Present:\t" + str(condProbIns[(ua, ub)])


if __name__ == "__main__":
    #main();
    summarizeCondProbMostActive(100)