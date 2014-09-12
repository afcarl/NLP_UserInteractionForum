import numpy as np
import userCommentLength
import matplotlib.pyplot as plt
import math
import userCommentLength;

def plotHists():
    textLenHistograms = userCommentLength.loadTextLenHistograms();
    for user in textLenHistograms:
        #print user
        seq = np.array([int(math.sqrt(num))for num in textLenHistograms[user]])
        maxVal = max(seq);
        hist = np.histogram(seq, bins=range(0,maxVal,2))
        fig = plt.figure();
        #print len(hist[1][0:0])
        #print len(hist[0])
        fig.suptitle("Histogram of Sqrt(Comment Length) for User " + user, fontsize=14, fontweight='bold')
        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)
        ax.plot(hist[1][0:-1], hist[0]);
        plt.show()
        
def plotCondHists(numFriends):
    conds = userCommentLength.loadCondTextLenHistograms();
    activeUsers = userCommentLength.loadMostActiveUsers(numFriends);
    for user in activeUsers:
        fig = plt.figure();
        fig.suptitle("Conditional Histograms of User " + user);
        axs = np.array([])
        for i in range(numFriends):
            sq = int(math.sqrt(numFriends))
            axs = np.append( axs,  fig.add_subplot(sq,sq,i+1))
        #ax1 = fig.add_subplot(331);
        #ax2 = fig.add_subplot(332);
        counter = 0;
        fig.subplots_adjust(top=0.85)
        for pair in conds:
            if pair[0] == user:
                user2 = pair[1];
                seq = np.array([int(math.sqrt(num))for num in conds[pair]])
                maxVal = max(seq)
                hist = np.histogram(seq, bins=range(0, maxVal, 2))
                axs[counter].plot(hist[1][0:-1], hist[0]);
                axs[counter].set_ylabel(user2)
                counter += 1;
                #ax1.plot()
        plt.show();
        

if __name__ == "__main__":
    #plotHists();
    plotCondHists(25);