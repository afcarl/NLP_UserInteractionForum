from __future__ import division
import numpy as np
import projectUtil
import pickle
import userCommentLength


def main():
    ts = projectUtil.loadData();
    mostActiveUsers = userCommentLength.loadMostActiveUsers(100)
    #constructConditionalHistograms(ts, 25)
    #constructUserClassFrequency(ts)
    userCategory = loadUserClassFrequency()
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
    userJointInsightful = loadJointCategory();
    #print(userJointInsightful)
    findThreadProbability(ts)
    threadnum = loadTotalThreadNum()
    print(threadnum)
    #print(totalThreadNum)
    
    
    
def constructUserClassFrequency(ts):
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
    pickle.dump(userCategory, open('Data/userClassFrequency.p','wb'))
    
def constructJointCategory(ts):
    print "Constructing Category"
    userCondFreqInsightful = {};
    userPairFreqAllClass = {};
    cats = {'Troll': 14932, 'Funny': 40672, 'None': 464104, 'Flamebait': 7456, 
            'Redundant': 4792, 'Offtopic': 11384, 'Informativ': 40188, 'Interestin': 50168, 
            'Insightful': 73864}
    for thread in ts:
        usersInThread = {};
        userClassFrequency = {};
        #first loop and get all the unique users, plus num insightful
        for comment in thread:
            if 'author' not in comment:
                continue; 
            # add comment['author'] to usersInThread
            if not (comment['author']) in usersInThread:
                usersInThread[comment['author']] = 1
            
            if 'modclass' not in comment:
                continue;            
            if not (comment['author'],comment['modclass']) in userClassFrequency:
                userClassFrequency[(comment['author'],comment['modclass'])] = 1
            else:
                userClassFrequency[(comment['author'],comment['modclass'])] += 1                
        #now use usersInThread and userClassFrequency to create key
        #Construct userCondFreqInsightful
        #Construct userPairFreqAllClass
        for userName1 in usersInThread:
            for userName2 in usersInThread:     
                # Insightful Frequency
                if not (userName1,'Insightful') in userClassFrequency:
                    pass;
                elif not (userName1 , userName2) in userCondFreqInsightful:
                    userCondFreqInsightful[(userName1, userName2)] = userClassFrequency[(userName1,'Insightful')]
                    print "New Value"
                    print userCondFreqInsightful[(userName1, userName2)] # debug
                else:
                    userCondFreqInsightful[(userName1, userName2)] += userClassFrequency[(userName1,'Insightful')]
                    print "Updating"
                    print userCondFreqInsightful[(userName1, userName2)] # debug
                # userName1 and userName2 are botn in thread
                
                # Total Frequencies
                for cat in cats:
                    if (userName1, cat) not in userClassFrequency:
                        pass;
                    elif not (userName1, userName2) in userPairFreqAllClass:
                        userPairFreqAllClass[(userName1, userName2)] = userClassFrequency[(userName1, cat)]
                    else:
                        userPairFreqAllClass[(userName1, userName2)] += userClassFrequency[(userName1, cat)]
                
    #pickle.dump(userCondFreqInsightful, open('Data/sortedUsersJointCategory.p','wb'))
    pickle.dump(userCondFreqInsightful, open('Data/usersConditionalFreqInsightful.p','wb'))  
    pickle.dump(userPairFreqAllClass, open('Data/userPairFrequencyAllClass.p','wb'))
    print "test1"
    for key in userCondFreqInsightful:
        print "Key" + str(key)
        print userCondFreqInsightful[key]
        print userPairFreqAllClass[key]
        userCondFreqInsightful[key] /= userPairFreqAllClass[key]
    pickle.dump(userCondFreqInsightful, open('Data/usersConditionalProbInsightful.p','wb'))  
    

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
    pickle.dump(totalThreadNum, open("Data/totalthreadnum.p","wb"))           
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


def loadConditionalProbInsightful():
    return pickle.load(open('Data/usersConditionalProbInsightful.p','rb'))

def loadUserClassFrequency():
    return pickle.load(open('Data/userClassFrequency.p','rb'))

def loadThreadProbabilityEachUser():
    return pickle.load(open('Data/probUserPostInThread.p', 'rb'))

def loadUserPairFrequencyAllClass():
    return pickle.load(open('Data/userPairFrequencyAllClass.p','rb'))

def loadUserPairCondFreqInsightful():
    return pickle.load(open('Data/usersConditionalFreqInsightful.p','rb'))  

def loadTotalThreadNum():
    return pickle.load(open('Data/totalthreadnum.p','rb'))

if __name__ == "__main__":
    mainJoint();
