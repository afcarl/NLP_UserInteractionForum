import numpy as np
import projectUtil
import pickle

def getMostActiveUsers(ts, numActiveUsers=-1):
    users = {}; # will store the number of comments posted
    for t in ts:
        for comment in t:
            key = comment['author'];
            print "Text Length" +  str(comment['textLen']);
            if  key in users:
                users[key] += 1;
            else:
                users[key] = 1;
    sortedUsers = sorted(np.array([(user, users[user]) for user in users]) , key = lambda x: x[1]);
    import pickle
    pickle.dump(sortedUsers, open('Data/sortedUsersNumComments.p','wb'))
    if numActiveUsers < 0:
        return np.array([u[0] for u in sortedUsers])
    else:
        return np.array([u[0] for u in sortedUsers[-numActiveUsers:]]);

def constructHistograms(ts, numUsers):
    users = loadMostActiveUsers(numUsers);
    setUsers = set(users); # for fast membership test
    userHistograms = {};
    for thread in ts:
        for comment in thread:
            if comment['author'] in setUsers:
                if comment['author'] in userHistograms:
                    userHistograms[comment['author']] =  np.append(userHistograms[comment['author']], comment['textLen'])
                else:
                    userHistograms[comment['author']] = np.array([comment['textLen']])
    import pickle
    pickle.dump(userHistograms, open('Data/userTextLenHistogram.p','wb'))
    
    
    
def constructConditionalHistograms(ts, numUsers):
    users = loadMostActiveUsers(numUsers);
    print "Start Constructing Conditional Histogram"
    condHistograms = {};
    for user1 in users:
        for user2 in users:
            # if not (user1 == user2):
            print "."
            for thread in ts:
                if(threadContainsBothUsers(thread, user1, user2)):
                    # count number of user1's comment
                    for comment in thread:
                        if comment['author'] == user1:
                            if (user1, user2) in condHistograms:
                                condHistograms[(user1, user2)] = np.append(condHistograms[(user1, user2)], comment['textLen'])
                            else:
                                condHistograms[(user1, user2)] = np.array([comment['textLen']])
    import pickle
    pickle.dump(condHistograms, open('Data/userTextLenConditionalHistogram.p','wb'))
    
def threadContainsBothUsers(thread, user1, user2):
    user1_in = False;
    user2_in = False
    for comment in thread:
        if comment['author'] == user1:
            user1_in = True;
        if comment['author'] == user2:
            user2_in = True;
        if user1_in and user2_in:
            break;
    return (user1_in and user2_in)


def constructHistogramsConditional(ts, users):
    pass;

def loadUserNumComment():
    return pickle.load(open('Data/sortedUsersNumComments.p','rb'));

def loadTextLenHistograms():
    return pickle.load(open('Data/userTextLenHistogram.p','rb'));

def loadCondTextLenHistograms():
    return pickle.load(open('Data/userTextLenConditionalHistogram.p','rb'))

def loadMostActiveUsers(numUsers= -1):
    allUsers = loadUserNumComment();
    if numUsers == -1:
        return np.array([u[0] for u in allUsers])
    else:
        return np.array([u[0] for u in allUsers[-numUsers:]])
    

def main():
    ts = projectUtil.loadData();
    # First: find 100 most active users (counting the number of comments)
    #mostActiveUsers = getMostActiveUsers(ts,10);
    #print mostActiveUsers;
    #constructHistograms(ts, mostActiveUsers);
    constructConditionalHistograms(ts, 25)


if __name__ == "__main__":
    main();
