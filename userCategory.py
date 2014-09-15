from __future__ import division
import numpy as np
import projectUtil
import pickle
import userCommentLength


def main():
    ts = projectUtil.loadData();
    mostActiveUsers = userCommentLength.loadMostActiveUsers(100)
    #constructConditionalHistograms(ts, 25)
    #constructCategory(ts)
    userCategory = loadconstructCategory()
    [userInsightful, numTotalPosts] = findInsightful(userCategory)
    for user in mostActiveUsers:
        print user;
        if user in userInsightful:
            print userInsightful[user]
            print numTotalPosts[user]
    
def mainJoint():
    ts = projectUtil.loadData();
    mostActiveUsers = userCommentLength.loadMostActiveUsers(100)
    constructJointCategory(ts)
    #userJointInsightful = loadJointCategory();
    #print(userJointInsightful)
    
    
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
    userJointCategory = {};
    userTotalCategory = {};
    cats = {'Troll': 14932, 'Funny': 40672, 'None': 464104, 'Flamebait': 7456, 
            'Redundant': 4792, 'Offtopic': 11384, 'Informativ': 40188, 'Interestin': 50168, 
            'Insightful': 73864}
    for thread in ts:
        uniqueUsers = {};
        userCategory = {};
        #first loop and get all the unique users, plus num insightful
        for comment in thread:
            if 'author' not in comment:
                continue; 
            if not (comment['author']) in uniqueUsers:
                uniqueUsers[comment['author']] = 1
            if 'modclass' not in comment:
                continue;            
            if not (comment['author'],comment['modclass']) in userCategory:
                userCategory[(comment['author'],comment['modclass'])] = 1
            else:
                userCategory[(comment['author'],comment['modclass'])] += 1                
        #now use uniqueUsers and userCategory to create key
        for userName1 in uniqueUsers:
            for userName2 in uniqueUsers:
                #ask ben how to find insightful posts for userName1 from userCategory
                #then can do key
                
                if not (userName1,'Insightful') in userCategory:
                    continue;
                if not (userName1 , userName2) in userJointCategory:
                    userJointCategory[(userName1, userName2)] = userCategory[(userName1,'Insightful')]
                else:
                    userJointCategory[(userName1, userName2)] += userCategory[(userName1,'Insightful')]
                
                for cat in cats:
                    if (userName1, cat) not in userCategory:
                        continue;
                    if not (userName1, userName2) in userTotalCategory:
                        userTotalCategory[(userName1, userName2)] = userCategory[(userName1, cat)]
                    else:
                        userTotalCategory[(userName1, userName2)] += userCategory[(userName1, cat)]
                
    #pickle.dump(userJointCategory, open('Data/sortedUsersJointCategory.p','wb'))
    pickle.dump(userTotalCategory, open('Data/sortedUsersTotalCategory.p','wb'))
    print "test1"
    for key in userJointCategory:
        userJointCategory[key] /= userTotalCategory[key]
    pickle.dump(userJointCategory, open('Data/sortedUsersJointProbInsightful.p','wb'))  
    
    userThreadProb = findThreadProbability(ts);
    userConditionalProbInsightful = {};
    print "test2"
    for key in userJointCategory:
        userConditionalProbInsightful[key] = userJointCategory[key]/(userThreadProb[key[1]]) 
    pickle.dump(userConditionalProbInsightful, open('Data/sortedUsersConditionalProbInsightful.p','wb'))  

def findThreadProbability(ts):
    print "Finding Probability"
    userThreadProb = {};
    totalThreadNum = 0;
    for thread in ts:
        totalThreadNum +=1;
        localDict = {};
        for comment in thread:
            if 'author' not in comment:
                continue
            elif comment['author'] in localDict:
                continue
            else:
                localDict[comment['author']] = 1;
        for key in localDict:
            if key in userThreadProb:
                userThreadProb[key] += 1;
            else:
                userThreadProb[key] = 1;
    for key in userThreadProb:
        userThreadProb[key] /= totalThreadNum
    pickle.dump(userThreadProb, open("Data/probUserPostInThread.p", "wb"))
    return userThreadProb;

        
        
        
            
 
 
    
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

def loadJointCategory():
    return pickle.load(open('Data/sortedUsersJointCategory.p','rb'))

def loadconstructCategory():
    return pickle.load(open('Data/sortedUsersCategory.p','rb'))


if __name__ == "__main__":
    mainJoint();
