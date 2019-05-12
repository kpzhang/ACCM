# -*- coding: UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
#listdir
from os import listdir
#random
import sys
import re
import cal
import random
from random import shuffle
#word2vec
from gensim import corpora,models,similarities
from gensim import utils,matutils
from gensim.models import word2vec
from gensim import *
#START是主函数
def start(father="data10/",changeRate=0.1,filename='x.txt'):
	#第一部分：获得changey.txt
	fx=open(filename)
	fc=open(father+'changey.txt','w')
	fy=open(father+'y2.txt','w')
	biggestNode=1
	nowIter=0
	nodeSet=set()
	nodeSet2=set()
	#randomIter=random.randint(0,9)

	#1.-浏览边
	for line in fx.readlines():
		lineArr = re.split(' |,',line.strip())#以空格分开,每一条边记录到
                lenth=len(lineArr)
                if(lenth<2): #捕获最后一行空的情况
                    break;


		fc.write('%s %s\n'%(lineArr[0],lineArr[1]))
		nodeSet.add(int(lineArr[0]))
		nodeSet.add(int(lineArr[1]))
		nodeSet2.add(int(lineArr[0]))
		nodeSet2.add(int(lineArr[1]))
		#if(int(lineArr[0])>biggestNode):#记录数字最大的节点
			#biggestNode=(lineArr[0])
                
		nowIter+=1
        biggestNode=max(nodeSet2)
        print "biggestNode=",biggestNode
	#2.随机删除changeRate%的节点，和所有相关的边
	fc.close()
	fc=open(father+'changey.txt','r')
	removeSet=set()
        lenSet=int(len(nodeSet))
        nowIter=0
        nodeSet=list(nodeSet)
        random.Random(0).shuffle(nodeSet)

     #随机选择要删除的节点
        for nowIter in range(int(changeRate*lenSet)):
            node=random.Random().choice(nodeSet)
            removeSet.add(node)
            nodeSet2.remove(node)
            nodeSet.remove(node)
        print "len(removeSet)=",len(removeSet)
	#删除节点相关联的边
	for line in fc.readlines():
	    lineArr = re.split(' |,',line.strip())#以空格分开,每一条边记录到
            lenth=len(lineArr)
            if(lenth<2): #捕获最后一行空的情况
                break;
	    if int(lineArr[0]) not in removeSet and int(lineArr[1]) not in removeSet:
		fy.write('a%s a%s\n'%(lineArr[0],lineArr[1]))
	print "removeSet=",removeSet
	#3.加changeRate的节点，每个节点加du条边
        #biggestNode=int(5000)
	newNode=int(biggestNode)#新加的节点在最大的数字后加1
	#alllen,du=cal.start(filename)
        alllen=11765;du=947;
	for j in range(int(changeRate*alllen)):
	    newNode+=1#新加的节点数字加1
	    i=0
	    nowIter=0
            nodeSet2=list(nodeSet2)
            random.Random(0).shuffle(nodeSet2)   #打乱顺序
            addset=set()
	    while(i < du):
                nodeY=random.Random().choice(nodeSet2)
                
		if(nodeY not in addset):
                    addset.add(nodeY)
		    fy.write('a%s a%s\n'%(newNode,nodeY))
                    #print "i=",i,":",newNode,"+",nodeY," "
		    i+=1

	ff=open(father+'connectY2.txt','w')
	for node in nodeSet2:
		ff.write('%s a%s\n'%(node,node))

	ff.close()
	fy.close()
	fc.close()
	fx.close()

if __name__=="__main__":
    nLen = len(sys.argv);
    for i in range(nLen):  
        print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    changeRate=float(sys.argv[2])
    filename=str(sys.argv[3])
    start(str(father),float(changeRate),str(filename))
