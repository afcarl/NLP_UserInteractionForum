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

def extractHTML(direcs=["Data/Slashdot/slashdot_part_1","Data/Slashdot/slashdot_part_1"]):
    from bs4 import BeautifulSoup
    for direc in direcs:
        for datafile in os.listdir(direc):
            if(datafile == ".DS_Store"):
                continue;
            filepath = os.path.join(direc, datafile);
            soup = BeautifulSoup(open(filepath));
            print "Processing File:\t" + datafile;
            for child in soup.recursiveChildGenerator():
                name = getattr(child, "name", None)
                if name is not None:
                    print "Name not None"
                    print name
                elif not child.isspace(): # leaf node, don't print spaces
                    print "childNotSpace"
                    print child
            break;

def aggregateClassFrequency(folders=["Data/Slashdot/slashdot_part_1","Data/Slashdot/slashdot_part_1"]):
    theDict = {};
    dominatingClassDict = {};
    for folder in folders:
        for datafile in os.listdir(folder):
            if(datafile == ".DS_Store"):
                continue;
            fileDict = fileClassFrequency(os.path.join(folder,datafile));
            domClass = max(dict(fileDict.items() + {'None':-1000000000}.items()).iteritems(), key=operator.itemgetter(1))[0]
            #print "Before"
            #print domClass
            #print dominatingClassDict
            dominatingClassDict = mergeDicts(dominatingClassDict, {domClass:1});
            #print "After"
            #print dominatingClassDict
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



if __name__ == "__main__":
    extractHTML();
    
