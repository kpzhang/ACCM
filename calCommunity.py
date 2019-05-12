# -*- coding:  UTF-8 -*-
from numpy import *
import operator
import sys;
import re
from os import listdir
import random
from random import shuffle

def loadGraphDict(father='data/',fileName='x3.txt'):
    dataDict = {}
    fx = open(father+fileName)
    j=0
    for line in fx.readlines():
        lineArr = re.split(' |,|\t',line.strip())
        lenth=len(lineArr)
        if(j%10000==0):print 'j=',j
        j+=1
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


def loadCircleDict(father='data/',fileName='x3.txt'):
    communityID=0
    communityDict={}
    communityDict['0']=0
    fx = open(father+fileName)
    j=0
    for line in fx.readlines():#
        lineArr = re.split(' |,|\t',line.strip())#
        lenth=len(lineArr)
        if(j%10000==0):print 'i=',j
        j+=1
        if(lenth<1): 
            break;
        if(lineArr[0] not in communityDict.keys() and lineArr[1] not in communityDict.keys()):
            communityID+=1
            communityDict[str(lineArr[0])]=communityID
            communityDict[str(lineArr[1])]=communityID
            continue;
        if(lineArr[0] in communityDict.keys() and lineArr[1] in communityDict.keys()):
            communityID+=1
            a=communityDict[str(lineArr[0])];
            b=communityDict[str(lineArr[1])];
            if(a!=b):
                if(a>b):big=a;small=b;
                else: big=b;small=a;
                for k in communityDict.keys():
                    if(communityDict[k]==big):
                        communityDict[k]=small
                print small,'=',big
                f1=open(father+'hebing.txt','a')
                f1.write('%d=%d\n'%( small,big ))
                f1.close()
            continue;
        if(lineArr[0] in communityDict.keys()):
            communityDict[str(lineArr[1])]=communityDict[str(lineArr[0])]
            continue;
        if(lineArr[1] in communityDict.keys()):
            communityDict[str(lineArr[0])]=communityDict[str(lineArr[1])]
            continue;    
    return communityDict

def start(father='data/',fileName='x3.txt'):

    communityDict=loadCircleDict(father,fileName)
    fww=open(father+'community1_t.txt','w')
    for k in communityDict.keys():
        fww.write('%s\t%d\n'%(k,communityDict[k] ) )
    fww.close()
    dataDict=loadGraphDict(father,fileName);
    fwww=open(father+'communitydu_t.txt','w')
    for k in dataDict.keys():
        fwww.write('%s\t%d\t%d\n'%(k,communityDict[k],len(dataDict[k]) ) )
    fwww.close()
    return 0

if __name__=="__main__":
    start(father='data/',fileName='twitter_following')
