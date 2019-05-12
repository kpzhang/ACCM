# -*- coding:  UTF-8 -*-
from numpy import *
import operator
import sys
import re
from os import listdir

def loadGraphDict(fileName):
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines():
        lineArr = re.split(' |,|\t',line.strip())
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


def start(filename):
    xDict=loadGraphDict(filename)
    i=0
    sumdu=0.0
    for node in xDict.keys():
        sumdu+=len(xDict[node])
        i+=1
    print("items="),i
    print("average degree="),float(sumdu/i)

    fp=open('data/xDict.txt','w')
    for li,lis in xDict.items():
        fp.write('%s '%str(li))
        for h in lis:
            fp.write('%s '%str(h))
        fp.write('\n')
    fp.close()

    return i,float(sumdu/i),xDict


if __name__=="__main__":
    filename=sys.argv[1]
    start(filename)
