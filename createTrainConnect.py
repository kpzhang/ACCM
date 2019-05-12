# -*- coding:  UTF-8 -*-
#
from numpy import *
#
import operator
import sys;
import re
import cal
#import change
#listdir
from os import listdir
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *


#
def loadGraphDict(fileName):#
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines():#
        lineArr = re.split(' |,|\t',line.strip())#
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict.keys()):
            dataDict[str(lineArr[0])]=[str(lineArr[1])]
#
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict[str(lineArr[0])]):
            dataDict[str(lineArr[0])].append(str(lineArr[1]))
#
    #
        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]=[str(lineArr[0])]#
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict[str(lineArr[1])]):
            dataDict[str(lineArr[1])].append(str(lineArr[0]))#
    return dataDict




#
def start():
    #father="data/"
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    filename=str(sys.argv[2])

    fx=open(father+'connect.txt')
    fc=open(father+'trainConnect.txt','w')
    ft=open(father+'testConnect.txt','w')

    randomIter=random.randint(0, 3)
    nowIter=0
    i=0
    for line in fx.readlines():
	lineArr = line.strip().split()
        if(nowIter==randomIter):
            nowIter+=1;
	    #if(len(xDict[lineArr[0]])>10):
	    ft.write('%s %s\n'%(lineArr[0],lineArr[1]))
        else:
            nowIter+=1;
	    #if(len(xDict[lineArr[0]])>10):
	    fc.write('%s %s\n'%(lineArr[0],lineArr[1]))
	if(nowIter>=3):
            randomIter=random.randint(0, 3);
            nowIter=0
	i+=1
    print("items="),i
    fc.close()
    ft.close()

if __name__=="__main__":
    start()
