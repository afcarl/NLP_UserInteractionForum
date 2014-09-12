import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import re
import operator

def uta(a):
    return a;

# will discard
def utaa(uString):
    from bs4 import BeautifulSoup
    print uString
    print type(uString)
    soup = BeautifulSoup(uString); 
    newUString = ''.join(soup.findAll(text=True));
    import unicodedata
    return unicodedata.normalize('NFKD', newUString).encode('ascii','ignore');

def extract_tree_data(direc="Data/Slashdot/slashdot_part_1"):
    for datafile in os.listdir(direc):
        if(datafile == ".DS_Store"):
            continue;
        print datafile
        tree = ET.parse(os.path.join(direc, datafile));
        print tree
        # error because it's not actually an XML file
        # take a look at the structure later
        break;

# This method is only used once to load data and save it into a pickle file
def extractHTML(direcs=["Data/Slashdot/slashdot_part_1","Data/Slashdot/slashdot_part_1"]):
    from bs4 import BeautifulSoup
    dicts = [];
    for direc in direcs:
        ## DEBUG
        i = 1;
        for datafile in os.listdir(direc):
            if(datafile == ".DS_Store"):
                continue;
            filepath = os.path.join(direc, datafile);
            soup = BeautifulSoup(open(filepath));
            print "Processing File:\t" + datafile;
            fileSequence = [];
            for el in soup.find_all("article"):
                d = {};
                d['id'] = uta(el.find("id").renderContents())
                d['title'] = uta(el.find("title").renderContents());
                d['author'] = uta(el.find("author").renderContents());
                d['datestamp'] = uta(el.find("datestamp").renderContents());
                # prefer sentencetext to htmltext
                # but use htmltext if sentencetext does not exist
                t = el.find("htmltext");
                if t is not None and len(t.renderContents()) > 0:
                    text = t.renderContents()
                else:
                    text = el.find("htmltext").renderContents()
                d['textLen'] = len(text);
                d['type'] = "article"
                fileSequence.append(d);
            for el in soup.find_all("comment"):
                #print el
                d = {};
                d['id'] = uta(el.find("id").renderContents())
                d['title'] = uta(el.find("title").renderContents())
                d['author'] = uta(el.find("author").renderContents())
                d['datestamp'] = uta(el.find("datestamp").renderContents())
                d['modclass'] = uta(el.find("modclass").renderContents())
                d['modscore'] = uta(el.find("modscore").renderContents())
                # prefer sentencetext to htmltext
                # but use htmltext if sentencetext does not exist
                t = el.find("htmltext");
                if t is not None and len(t.renderContents()) > 0:
                    text = t.renderContents()
                else:
                    text = el.find("htmltext").renderContents()
                d['textLen'] = len(text);
                if(len(text) < 2):
                    print text;
                d['type'] = "comment"
                
                fileSequence.append(d);
            dicts.append(fileSequence);
    import pickle
    pickle.dump(dicts, open("Data/processedData.p", "wb"))
    return dicts                    

def aggregateClassFrequency(folders=["Data/Slashdot/slashdot_part_1","Data/Slashdot/slashdot_part_1"]):
    theDict = {};
    dominatingClassDict = {};
    for folder in folders:
        for datafile in os.listdir(folder):
            if(datafile == ".DS_Store"):
                continue;
            fileDict = fileClassFrequency(os.path.join(folder,datafile));
            domClass = max(dict(fileDict.items() + {'None':-1000000000}.items()).iteritems(), key=operator.itemgetter(1))[0]
            dominatingClassDict = mergeDicts(dominatingClassDict, {domClass:1});
            theDict = mergeDicts(theDict, fileDict);
            
    return [theDict, dominatingClassDict];

def fileClassFrequency(filepath):
    # read the class between <modclass>
    fileDict = {};
    f = open(filepath, 'r');
    strings = re.findall(r'<modclass>(.*)</modclass>', f.read());
    for string in strings:
        if not string in fileDict:
            fileDict[string] = 1;
        else:
            fileDict[string] += 1;
    return fileDict
    

def main():
    [theDict, aggregateDict] = aggregateClassFrequency()
    print "Final Result"
    print theDict
    print aggregateDict


def mergeDicts(d1, d2):
    combinedDict = {};
    for key in d1:
        combinedDict[key] = d1[key];
    for key in d2:
        if not key in combinedDict:
            combinedDict[key] = d2[key];
        else:
            combinedDict[key] += d2[key];
    return combinedDict;

def loadData():
    import pickle;
    return pickle.load(open("Data/processedData.p","rb"));

def loadFullTextData():
    import pickle;
    return pickle.load(open("Data/processedFullTextData.p","rb"));

if __name__ == "__main__":
    dicts = extractHTML();
    print "The number of threads processed:\t" + str(len(dicts))
    