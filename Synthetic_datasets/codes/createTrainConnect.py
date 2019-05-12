# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys;
import re
#listdir
from os import listdir
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
            dataDict[str(lineArr[0])]={str(lineArr[1]):0}#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict[str(lineArr[0])].keys()):
            dataDict[str(lineArr[0])][str(lineArr[1])]=0#在该节点的相邻边集上加一条新边
    #有向图则只一边，无向图加两次。
        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]={str(lineArr[0]):0}#建立以某个节点的相邻边集权重字典
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict[str(lineArr[1])].keys()):
            dataDict[str(lineArr[1])][str(lineArr[0])]=0#在该节点的相邻边集上加一条新边
    return dataDict



#START是主函数
def start():
    #father="data20/"
    nLen = len(sys.argv);
    for i in range(0, nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    filename=str(sys.argv[2])
    #第一部分：获得图中边的字典表示
    ###xDict=loadGraphDict(filename)
    #print "xDict=",xDict
    ###yDict=loadGraphDict(father+'y2.txt')
    #print "yDict=",yDict

    fx=open(father+'connectY2.txt')
    fc=open(father+'trainConnect.txt','w')
    ft=open(father+'testConnect.txt','w')

    randomIter=random.randint(0, 3)
    nowIter=0
    i=0
    for line in fx.readlines():
	lineArr = line.strip().split()
        if(nowIter==randomIter):
            nowIter+=1;
	    ###if(len(xDict[lineArr[0]])>0):
	    ft.write('%s %s\n'%(lineArr[0],lineArr[1]))
        else:
            nowIter+=1;
	    ###if(len(xDict[lineArr[0]])>0):
	    fc.write('%s %s\n'%(lineArr[0],lineArr[1]))
	if(nowIter>=3):
            randomIter=random.randint(0, 3);
            nowIter=0
	i+=1
    print("共有几条="),i
    fc.close()
    ft.close()

if __name__=="__main__":
    start()
