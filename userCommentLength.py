import numpy as np
import projectUtil

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

def constructHistograms(ts, users):
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
    
    
    
def constructConditionalHistograms(ts, users):
    setUsers = set(users);
    condHistograms = {};
    #import pickle
    #pickle.dump(condHistograms, open('Data/small_userTextLenConditionalHistogram.p','wb'))
    
def constructHistogramsConditional(ts, users):
    pass;

def loadUserNumComment():
    import pickle
    return pickle.load(open('Data/sortedUsersNumComments.p','rb'));

def loadTextLenHistograms():
    import pickle
    return pickle.load(open('Data/userTextLenHistogram.p','rb'));

def main():
    ts = projectUtil.loadData();
    # First: find 100 most active users (counting the number of comments)
    mostActiveUsers = getMostActiveUsers(ts,10);
    print mostActiveUsers;
    constructHistograms(ts, mostActiveUsers);


if __name__ == "__main__":
    main();