# -*- coding:  UTF-8 -*-

from numpy import *

import operator
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt

from os import listdir

from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim import *

def loadGraphDict(fileName):
    dataDict = {}
    fx = open(fileName)
    for line in fx.readlines():#m lines
        try:
            lineArr = re.split(' |,',line.strip())
            lenth=len(lineArr)
        except Exception:
            print "The last line is empty";break;
        if(lenth<2): 
            break;
        if(lineArr[0] not in dataDict.keys()):
            dataDict[str(lineArr[0])]={str(lineArr[1]):0}
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[1] not in dataDict[str(lineArr[0])].keys()):
            dataDict[str(lineArr[0])][str(lineArr[1])]=0

        if(lineArr[1] not in dataDict.keys()):
            dataDict[str(lineArr[1])]={str(lineArr[0]):0}
        #elif(len(dataDict[str(lineArr[0])])>0)
        if(lineArr[0] not in dataDict[str(lineArr[1])].keys()):
            dataDict[str(lineArr[1])][str(lineArr[0])]=0
    return dataDict


def start(filename):
    xDict=loadGraphDict(filename)
    G=nx.Graph()

    for node in xDict.keys():
        G.add_node(node)

    for node1 in xDict.keys():
        for (node2,dis) in xDict[node1].items():#
            G.add_edge(str(node1), str(node2))

    pos=nx.spring_layout(G)

    G.to_undirected() 
    nx.draw(G,with_labels=True,node_size=20,node_color='g',edge_color='g',font_color='r',font_size=15)
    plt.savefig("pic3.png") 
    plt.show()

if __name__=="__main__":
    filename=sys.argv[1]
    start(filename)
