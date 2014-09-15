from __future__ import division
import numpy as np
import projectUtil
import pickle
import userCommentLength


def main():
    ts = projectUtil.loadData();
    mostActiveUsers = userCommentLength.loadMostActiveUsers(100)
    # constructConditionalHistograms(ts, 25)
    #constructCategory(ts)
    userCategory = loadconstructCategory()
    [userInsightful, numTotalPosts] = findInsightful(userCategory)
    #for user in numTotalPosts:
    #    if numTotalPosts[user] > 50:
    #        print user + " num post=\t" + str(numTotalPosts[user]) + " prob insightful:\t" + str(userInsightful[user])
    for user in mostActiveUsers:
        print user;
        if user in userInsightful:
            print userInsightful[user]
            print numTotalPosts[user]
    
def constructCategory(ts):
    print "Constructing Category"
    userCategory = {};
    for thread in ts:
        for comment in thread:
            print "."
            if 'modclass' not in comment:
                continue;            
            if not (comment['author'],comment['modclass']) in userCategory:
                userCategory[(comment['author'],comment['modclass'])] = 1
            else:
                userCategory[(comment['author'],comment['modclass'])] += 1
    pickle.dump(userCategory, open('Data/sortedUsersCategory.p','wb'))
    
def constructJointCategory(ts):
    print "Constructing Category"
    userCategory = {};
    for thread in ts:
        for comment in thread:
            print "."
            if 'modclass' not in comment:
                continue;            
            key = (comment['author'], otherUser, comment['modclass'])
            if not key in userCategory:
                userCategory[key] = 1
            else:
                userCategory[key] += 1
    pickle.dump(userCategory, open('Data/sortedUsersCategory.p','wb'))

def findInsightful(userCategory):
    print "Finding Insightful"
    insightfulDict = {}
    totalDict = {}
    for pairedUserClass in userCategory:
        user = pairedUserClass[0]
        cla = pairedUserClass[1]
        #print "User :" + user;
        #print "Class:" + cla;
        if cla == "Insightful":
            insightfulDict[user] = userCategory[(user,cla)]
        
        if user in totalDict:
            totalDict[user] += userCategory[(user,cla)]
        else:
            totalDict[user] = userCategory[(user,cla)]
    
    for user in insightfulDict:
        numTotal = totalDict[user]
        insightfulDict[user] /= numTotal
    return [insightfulDict, totalDict];



def loadconstructCategory():
    return pickle.load(open('Data/sortedUsersCategory.p','rb'))


if __name__ == "__main__":
    main();
