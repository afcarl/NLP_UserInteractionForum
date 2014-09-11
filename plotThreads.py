import numpy as np
import matplotlib.pyplot as plt
import re
import projectUtil

def plotThreads(threads):
    #textLentghs = np.array((len(dicts), 1000));
    for thread in threads:
        numReps = len(thread);
        print thread;
        thread = sorted(thread, key= lambda x: int(x['datestamp']));
        #sorts each thread based on time (ascending)
        
        time_array = np.array([int(el['datestamp']) for el in thread]);
        length_array = np.array([int(el['textLen']) for el in thread]);
        modscore_array = np.array([(el['modscore'] if 'modscore' in el else 5) for el in thread])
        modclass_array = np.array([(el['modclass'] if 'modclass' in el else "None") for el in thread])
        modclass_binary = np.array([]);
        
        plt.figure();
        #plt.plot(range(numReps), timeStamp);
        #plt.plot(range(numReps), length_array);
        plt.plot(range(numReps), modscore_array);
        plt.show();
        
    


if __name__ == "__main__":
    #threads = projectUtil.extractHTML();
    threads = projectUtil.loadData();
    print "Finished Loading Data"
    plotThreads(threads)