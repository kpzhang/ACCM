# -*- coding:  UTF-8 -*-
#
import mpi4py.MPI as MPI
from numpy import *
import numpy as np 
import operator
import sys;
import time
import gc;
#listdir
from os import listdir
#word2vec
from gensim import corpora, models, similarities
from gensim import utils, matutils
from gensim.models import word2vec
from gensim.models import Word2Vec
from gensim import *



#global variables
comm=MPI.COMM_WORLD
comm_rank=comm.Get_rank()
comm_size=comm.Get_size()


#
#
def predict(trainlist,predictPair,modelX,modelY,W,father):
    bigdis=0
    for line in trainlist:
	nodeX=line
        if nodeX in modelX.vocab.keys():
	    vecX=[]
	    vecX=list(modelX[nodeX]);
	    vecX.append(1);
	    vecX=array(vecX)

	    vecXinY=vecX*W
	    minDistance=inf
	    
	else:	print nodeX;continue
	for nodeY in modelY.vocab.keys():
	    vecY=list(modelY[nodeY]);
	    vecY.append(1);
	    vecY=array(vecY)
	    distance=abs(sum((vecXinY-vecY)*(vecXinY-vecY).T))
	    if(distance<minDistance):
		minDistance=distance
		minDistanceNodeY=nodeY
	    else:
		continue
	predictPair[nodeX]=minDistanceNodeY

    return 0
#
def tpredict(local_testlist,tpredictPair,modelX,modelY,W,bigdis,father):

    for line in local_testlist:
	nodeX=line
        if nodeX in modelX.vocab.keys():
	    vecX=[]
	    vecX=list(modelX[nodeX]);
	    vecX.append(1);
	    vecX=array(vecX)
	    vecXinY=(vecX*W)
	    minDistance=inf
	    disDict={}
	    disDictnode=list()
	    disDictdis=list()
	else:	continue
	for nodeY in modelY.vocab.keys():
	    vecY=list(modelY[nodeY]);
	    vecY.append(1);
	    vecY=array(vecY)
	    distance=abs(sum((vecXinY-vecY)*(vecXinY-vecY).T))
	    disDictnode.append(str(nodeY))
	    disDictdis.append(float(distance))

	i=0

	for index in np.argpartition(disDictdis,kth=100)[:100]:
            eachKey=disDictnode[index];distance=disDictdis[index];
	    if(i==0):
		tpredictPair[nodeX]={eachKey:distance}
		i+=1
	    elif(i<100):
		i+=1
		tpredictPair[nodeX][eachKey]=distance
	    else:
		break
	del(disDictnode,disDictdis)
    return 0




def start(father):
    if comm_rank==0:
        #time
        gc.collect()
        print "startTime",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        #modelX=word2vec.Word2Vec.load_word2vec_format(father+"lx1_tang15_undirect_iter15_wind4_400s.emb", binary=False,fvocab=father+'modelx.vocab')       
        #modelY=word2vec.Word2Vec.load_word2vec_format(father+"ly1_tang15_iter15_wind4_400s.emb", binary=False,fvocab=father+'modely.vocab')

        #
        walkListX=word2vec.LineSentence(father+'walk1all_X.txt')#'walkListX.txt')
        modelX=Word2Vec(walkListX,negative=10,sg=1,hs=0,size=400,window=3,min_count=0,workers=5,iter=5)

        #del(walkListX)
        
        walkListY = word2vec.LineSentence(father+'walk1all_Y.txt')#'walkListY.txt')
        modelY=Word2Vec(walkListY,negative=10,sg=1,hs=0,size=400,window=3,min_count=0,workers=5,iter=5)


        gc.collect()

        ###modelX.init_sims(replace=True);modelY.init_sims(replace=True)
        modelX.save_word2vec_format(father+'lx1_tang8_direct_iter5_wind3_400s.emb', binary=False, fvocab=father+'modelx.vocab')
        modelY.save_word2vec_format(father+'ly1_tang8_direct_iter5_wind3_400s.emb', binary=False, fvocab=father+'modely.vocab')
        print "save ok !";
        gc.collect()

         
        #
        #
        realPairD={}
        fr = open(father+'trainConnect3148.txt_0')
        for line in fr.readlines():#m lines
            lineArr = line.strip().split()#
            if(lineArr[0] not in realPairD.keys()):
                realPairD[str(lineArr[0])]=str(lineArr[1])#
                #realPairD[str(lineArr[0])]=str(lineArr[0])#
            else:
                continue
        #
        matX = [];matY=[]
        for realPairX,realPairY in realPairD.items():
	    if(realPairX in modelX.vocab.keys() and realPairY in modelY.vocab.keys()):

	        listX=list(modelX[realPairX]);
	        listX.append(1);

	        listY=list(modelY[realPairY]);
	        listY.append(1)
	        matX.append(listX)
	        matY.append(listY)
        matX=matrix(matX);matY=matrix(matY)
        #
        xTx=matX.T*matX
        #W=eye(mysize+1)
        W=linalg.solve(xTx,matX.T*matY)

        #
        del(realPairD)
        del(matX,matY)
        gc.collect()
        print "trainOK Time:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #print "W=",W
    
        #
      
        bigdis=0
        all_trainlist=list();all_trainYlist=list()
        ft=open(father+'trainConnect3148.txt_0','r')
        for line in ft.readlines():
	    lineArr = line.strip().split()
	    nodeX=lineArr[0]
    	    #nodeY=lineArr[0]
    	    nodeY=lineArr[1]        
            all_trainlist.append(nodeX)
            all_trainYlist.append(nodeY)
        ft.close()

        all_testlist=list();all_testYlist=list()
        ft=open(father+'testConnect3148.txt_0','r')
        for line in ft.readlines():
	    lineArr = line.strip().split()
	    nodeX=lineArr[0]
    	    nodeY=lineArr[0]
	    #nodeY=lineArr[1]
            all_testlist.append(nodeX)
            all_testYlist.append(nodeY)
        ft.close()
        
        print "*******************trainset*******************"

    #0
    all_trainlist=comm.bcast(all_trainlist if comm_rank==0 else None,root=0)
    all_trainYlist=comm.bcast(all_trainYlist if comm_rank==0 else None,root=0)
    W=comm.bcast(mat(W) if comm_rank==0 else None,root=0)
    modelX=comm.bcast(modelX if comm_rank==0 else None,root=0)
    modelY=comm.bcast(modelY if comm_rank==0 else None,root=0)
    #
    num_samples=len(all_trainlist)
    
    local_trainlist_offset = np.linspace(0, num_samples, comm_size + 1).astype('int') 
    local_trainYlist_offset = np.linspace(0, num_samples, comm_size + 1).astype('int') 
     #
    local_trainlist = all_trainlist[local_trainlist_offset[comm_rank] :local_trainlist_offset[comm_rank + 1]]  
    local_trainYlist = all_trainYlist[local_trainYlist_offset[comm_rank] :local_trainYlist_offset[comm_rank + 1]] 
    print "****** %d/%d processor gets local data ****" %(comm_rank, comm_size)  
    #print local_trainlist

     
    #process in local  
    local_predictPair={}
    local_bigdis=predict(local_trainlist,local_predictPair,modelX,modelY,W,father)
    local_trainrightItem=0.0
    for i in range(0,len(local_trainlist)):
        node=local_trainlist[i]
        #print node,":",predictPair[node]
        if(node not in local_predictPair.keys()):print 'node',node;continue
	if (local_trainYlist[i]==local_predictPair[node]):
	    local_trainrightItem+=1
    if(len(local_predictPair)>0):
        print "local pid : %d ,train right items：%d ,local train accuracy ： %f："%(comm_rank,local_trainrightItem,float(local_trainrightItem)/len(local_predictPair))
    else:
	print "error,train,division 0！！"    del(local_predictPair)
    all_trainrightItem = comm.reduce(local_trainrightItem, root = 0, op = MPI.SUM) 
    bigdis= comm.reduce(local_bigdis, root = 0, op = MPI.MIN) 
    if comm_rank == 0:  
        print "*** all_trainrightItem: ", all_trainrightItem
        print "************ result right items：******************",num_samples
        print "all right accuracy ：：",(float)(all_trainrightItem)/num_samples
########################test##################################
    all_testlist=comm.bcast(all_testlist if comm_rank==0 else None,root=0)
    all_testYlist=comm.bcast(all_testYlist if comm_rank==0 else None,root=0)
    num_testsamples=len(all_testlist)
    local_testlist_offset = np.linspace(0, num_testsamples, comm_size + 1).astype('int') 
    local_testYlist_offset = np.linspace(0, num_testsamples, comm_size + 1).astype('int') 
     #  
    local_testlist = all_testlist[local_testlist_offset[comm_rank] :local_testlist_offset[comm_rank + 1]]  
    local_testYlist = all_testYlist[local_testYlist_offset[comm_rank] :local_testYlist_offset[comm_rank + 1]]  
    #process in local
    local_tpredictPair={}
    tpredict(local_testlist,local_tpredictPair,modelX,modelY,W,bigdis,father)
    #
    local_testrightItem100=0.0;
    local_testrightItem30=0.0;
    local_testrightItem15=0.0;
    local_testright10=0.0
    local_testright8=0.0
    local_testright5=0.0
    local_testright3=0.0
    local_testright1=0.0
    #fr=open('result.txt','a')
    for j in range(0,len(local_testlist)):
        now=0.0
        node=local_testlist[j]
        if(node not in local_tpredictPair.keys()):print 'node',node;continue
        #fr.write('%s '%str(node))
	for(dictPnode,distance) in sorted(local_tpredictPair[node].items(),key=operator.itemgetter(1)):
            now+=1
            flag=0
            #fr.write('%s '%(str(dictPnode)))
	    if(local_testYlist[j]==dictPnode):
		local_testrightItem100+=1
		if(now==1): 
                    local_testright1+=1;flag=1
		if(now<=3): 
                    local_testright3+=1
		if(now<=5): 
                    local_testright5+=1
		if(now<=8): 
                    local_testright8+=1
		if(now<=10): 
                    local_testright10+=1
		if(now<=15):
		    local_testrightItem15+=1
		if(now<=30):
                    #flag=1
		    local_testrightItem30+=1
		break
        fr.write('\n')
      
    if(len(local_tpredictPair)>0):
	print "local_top100 test accuracy：",(local_testrightItem100/len(local_tpredictPair))
	print "local_top30 test accuracy：",(local_testrightItem30/len(local_tpredictPair))
	print "local_top15 test accuracy：",(local_testrightItem15/len(local_tpredictPair))
	print "local_top10 test accuracy：",(local_testright10/len(local_tpredictPair))
	print "local_top8 test accuracy：",(local_testright8/len(local_tpredictPair))
	print "local_top5 test accuracy：",(local_testright5/len(local_tpredictPair))
	print "local_top3 test accuracy：",(local_testright3/len(local_tpredictPair))
	print "local_top1 test accuracy：",(local_testright1/len(local_tpredictPair))
        print "local_test items：",(len(local_tpredictPair))
    else:
	print "local_error,test，division 0！！"
    del(local_tpredictPair)

    all_testrightItem100 = comm.reduce(local_testrightItem100, root = 0, op = MPI.SUM) 
    all_testrightItem30 = comm.reduce(local_testrightItem30, root = 0, op = MPI.SUM) 
    all_testrightItem15 = comm.reduce(local_testrightItem15, root = 0, op = MPI.SUM) 
    all_testright10 = comm.reduce(local_testright10, root = 0, op = MPI.SUM) 
    all_testright8 = comm.reduce(local_testright8, root = 0, op = MPI.SUM) 
    all_testright5 = comm.reduce(local_testright5, root = 0, op = MPI.SUM) 
    all_testright3 = comm.reduce(local_testright3, root = 0, op = MPI.SUM) 
    all_testright1 = comm.reduce(local_testright1, root = 0, op = MPI.SUM) 
    if comm_rank == 0:  
        print "all_top100 test accuracy：",float(all_testrightItem100)/num_testsamples
        print "all_top30 test accuracy：",float(all_testrightItem30)/num_testsamples
        print "all_top15 test accuracy：",float(all_testrightItem15)/num_testsamples
	print "all_top10 test accuracy：",float(all_testright10)/num_testsamples
	print "all_top8 test accuracy：",float(all_testright8)/num_testsamples
	print "all_top5 test accuracy：",float(all_testright5)/num_testsamples
	print "all_top3 test accuracy：",float(all_testright3)/num_testsamples
	print "all_top1 test accuracy：",float(all_testright1)/num_testsamples
        print "all_ test items：",(num_testsamples)
        print "compete and predict end time:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    del(modelX,modelY,W)
    #print "record over time:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    gc.collect()
if __name__=="__main__":
    print "mpi4py start !"
    if comm_rank == 0: 
        nLen = len(sys.argv);
        for i in range(0, nLen):  
            print("argv %d:%s" %(i, sys.argv[i]));  
    father=str(sys.argv[1])
    start(str(father))

