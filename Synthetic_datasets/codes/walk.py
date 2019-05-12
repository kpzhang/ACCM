# -*- coding:  UTF-8 -*-
from numpy import *
import operator
import sys;
import re
from os import listdir
#random
import random
from random import shuffle
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *

#
def loadGraphDict(fileName):
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines()
        lineArr = re.split(' |,',line.strip())
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict.keys()):
            dataDict[str(lineArr[0])]=[str(lineArr[1])]
        if(lineArr[1] not in dataDict[str(lineArr[0])]):
            dataDict[str(lineArr[0])].append(str(lineArr[1]))
        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]=[str(lineArr[0])]
        if(lineArr[0] not in dataDict[str(lineArr[1])]):
            dataDict[str(lineArr[1])].append(str(lineArr[0]))
    return dataDict

#
def walk(graphDict,num_paths,walkfile):
    walkList=[]
    f1=open(walkfile,'a+')
    for j in range(int(num_paths)): 
        nodes=list(graphDict.keys())
	random.Random(0).shuffle(nodes)   
    	for keyStartNode in nodes: 
            walkList.append(keyStartNode)
            nowLength=1
	    RandomWalk(graphDict,walkList,keyStartNode,nowLength)
            for e in walkList:
		f1.write('%s '%(e))
	    f1.write('\n');
            #print 'walkList=',walkList
            walkList=[]
    f1.close()
    return walkList

#2.1
def RandomWalk(graphDict,walkList,nowNode,nowLength,walkLength=40):
    if(nowLength>=walkLength):	
        return 0
    nowNode=random.Random().choice(graphDict[nowNode])   
    walkList.append(nowNode)
    RandomWalk(graphDict,walkList,nowNode,nowLength+1)




#START main function
def start(father,numpaths):
    #father="data/"
    xDict=loadGraphDict('data/ytb.txt')
    #print "xDict=",xDict
    yDict=loadGraphDict('data/y2.txt')
    #print "yDict=",yDict
    while(numpaths!='stop'):
    #
        try:
            numpaths=int(numpaths)
        except EXception:
            break;
        walkListX=walk(xDict,numpaths,walkfile=father+'walkListX.txt')
        walkListY=walk(yDict,numpaths,walkfile=father+'walkListY.txt')
        print "Please give the num of paths"
        numpaths = raw_input()


if __name__=="__main__":
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    numpaths=int(sys.argv[2])
    start(str(father),int(numpaths))
