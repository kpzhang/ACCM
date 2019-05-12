# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys;
import re
#listdir
from os import listdir
#random
import random
from random import shuffle
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *

#第一部分：获得图中边的字典表示
def loadGraphDict(fileName):#初始化待处理数据
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines():#m行
        lineArr = re.split(' |,',line.strip())#以空格分开,每一条边记录到
        lenth=len(lineArr)
        
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict.keys()):
            dataDict[str(lineArr[0])]=[str(lineArr[1])]
#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict[str(lineArr[0])]):
            dataDict[str(lineArr[0])].append(str(lineArr[1]))
#在该节点的相邻边集上加一条新边
    #有向图则只一边，无向图加两次。
        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]=[str(lineArr[0])]#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict[str(lineArr[1])]):
            dataDict[str(lineArr[1])].append(str(lineArr[0]))#在该节点的相邻边集上加一条新边
    return dataDict

#第二部分：根据图边字典进行（权重）随机游走得到序列集
def walk(graphDict,num_paths,walkfile):
    walkList=[]#每一项是一条路径
    f1=open(walkfile,'a+')
    for j in range(int(num_paths)): #暂且写成从所有节点开始外循环趟数
        nodes=list(graphDict.keys())
	random.Random(0).shuffle(nodes)   #打乱顺序
    	for keyStartNode in nodes: #暂且写成从每个节点开始循环
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

#2.1递归函数，每次根据权重走一步，走过的边不再走，但水平有限，暂且写个不管权重的随机游走，
def RandomWalk(graphDict,walkList,nowNode,nowLength,walkLength=40):
    #randomIter=random.randint(0, len(graphDict[nowNode]))
    if(nowLength>=walkLength):	
        return 0
    #nowNode1=1
    nowNode=random.Random().choice(graphDict[nowNode])
    #ik=0.0
    #if(nowNode1 in walkList[-1]):
        #ik+=1
        #nowNode1=random.Random().choice(graphDict[nowNode].keys())
    #nowNode=nowNode1    
    walkList.append(nowNode)
    RandomWalk(graphDict,walkList,nowNode,nowLength+1)

    #nowIter=0
    #for nextNode in graphDict[nowNode].keys():#
        #if(nowIter==randomIter):
	    #nowNode=nextNode
	    #walkList[-1].append(str(nowNode))
	    #RandomWalk(graphDict,walkList,nowNode,nowLength+1)
            #break
        #else:
            #nowIter+=1;continue



#START是主函数
def start(father,numpaths,filename='ytb.txt'):
    #father="data0/"
    #第一部分：获得图中边的字典表示
    xDict=loadGraphDict(filename)
    #print "xDict=",xDict
    yDict=loadGraphDict(father+'y2.txt')
    #print "yDict=",yDict
    while(numpaths!='stop'):
    #第二部分：根据图边字典进行随机游走得到序列集
        try:
            numpaths=int(numpaths)
        except EXception:
            break;
        walkListX=walk(xDict,numpaths,walkfile=father+'walkListX.txt')
    #print "walkListX=",walkListX
        walkListY=walk(yDict,numpaths,walkfile=father+'walkListY.txt')
    #print "walkListY=",walkListY
        print "请输入游走趟数numpaths"
        numpaths = raw_input()


if __name__=="__main__":
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    numpaths=int(sys.argv[2])
    filename=str(sys.argv[3])
    start(str(father),int(numpaths),str(filename))
