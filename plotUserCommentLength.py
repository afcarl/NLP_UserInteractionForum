import numpy as np
import userCommentLength
import matplotlib.pyplot as plt
import math

def main():
    import userCommentLength;
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
        

if __name__ == "__main__":
    main();