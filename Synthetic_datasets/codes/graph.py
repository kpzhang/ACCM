# -*- coding:  UTF-8 -*-
#科学计算包
from numpy import *
#运算符模块
import operator
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt
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
        try:
            lineArr = re.split(' |,',line.strip())#以空格分开,每一条边记录到
            lenth=len(lineArr)
        except Exception:
            print "捕获最后一行空的情况";break;
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
def start(filename):
    #father="data10/"
    #第一部分：获得图中边的字典表示
    xDict=loadGraphDict(filename)
    G=nx.Graph()
    #setNode=set()
    #fx = open(filename)
    #for line in fx.readlines():#m行
        #lineArr = re.split(' |,',line.strip())#以空格分开,每一条边记录到
        #lenth=len(lineArr)
        #if(lenth<2): 
            #break;
        #setNode.add(str(lineArr[0]))
        #setNode.add(str(lineArr[1]))

    for node in xDict.keys():
        G.add_node(node)
    #fx.close()
    #fx = open(filename)
    for node1 in xDict.keys():
        for (node2,dis) in xDict[node1].items():#m行
            G.add_edge(str(node1), str(node2))
    #fx.close()
    #pos=nx.random_layout(G)
    #pos=nx.shell_layout(G)
    #pos=nx.spectral_layout(G)
    pos=nx.spring_layout(G)
    #nx.draw_networkx_nodes(G,pos,with_labels=True,node_size=52)
    #nx.draw_networkx_edges(G,pos,with_labels=True,edge_color='b')
    #nx.draw(G,pos,with_labels=True)
    G.to_undirected() 
    nx.draw(G,with_labels=True,node_size=20,node_color='g',edge_color='g',font_color='r',font_size=15)
    plt.savefig("pic3.png") 
    plt.show()

if __name__=="__main__":
    filename=sys.argv[1]
    start(filename)
