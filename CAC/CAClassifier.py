import numpy as np
import os
import pandas as pd 
from  CABBH.settings import STATIC_DIR

selection=[False,
 False, False, True, False, False, False, False, False, True, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, True, True, True, False, False, False, False, False, False, True, False, True, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, True, False, False, False, True, False]
mask = [False,
 True, True, True, True, True, False, True, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]


def getNeighbors(i,state):
	stateExt = np.concatenate(([0],state,[0]))
	neighbors = stateExt[i:(i+3)]
	return neighbors

def arrayToInt(bitlist):
	out = 0
	for bit in bitlist:
		out = (out << 1) | int(bit)
	return out	

def transition(i,m,state):
	row = i
	col = arrayToInt(getNeighbors(i,state))
	return m[row][col]

def nextState(state,m):
	next = np.zeros(len(state)-1)
	for i in range(0,len(state)-1):
		next[i] = transition(i,m,state)
	return next

def sgn(x):
	if x > 0:
		return 1
	elif x == 0:
		return 0
	else:
		return -1



def fitness(tp,fp,g1,g2,ap,an):
	return (1-(tp/(tp+fp)))+(0.01*((g1+g2)/(len(ap)+len(an))))

def getDataset(filename):
	file = open(filename,'r')
	features = []
	for line in file:
		cArray = line.split(",")
		iArray = np.zeros(len(cArray))
		for i in range(0,len(cArray)):
			iArray[i] = int(cArray[i])
		features.append(iArray) 
	return features



def cellSumatory(m1,m2,state):
	total = 0
	for i in range(0,len(state)-1):
		total += transition(i,m1,state) - transition(i,m2,state)
	return total

def getClassification(m1,m2,state):
	
	return cellSumatory(m1,m2,state)





            
def create_Ms():
	file = os.path.join(os.path.join(STATIC_DIR,"csv_files"),"diabetesB.csv")
	
	train_set = pd.read_csv(file)
	train_set = train_set.drop('Unnamed: 0' , axis = 1)
	
	train_set = train_set.values
	print(len(train_set[0]))
	n = len(train_set[0])-1 
	m1 = np.zeros(shape=(n,8))
	m2 = np.zeros(shape=(n,8))
	for i in range(0,len(train_set)):
		for j in range(0,len(train_set[i])-1):
			row = j
			col = arrayToInt(getNeighbors(j,train_set[i]))
			if train_set[i][n-1] == 1:
				m1[row][col] += 1
			else:
				m2[row][col] += 1
		
	return m1,m2


def get_classifier():
    
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]
    
    train = pd.DataFrame(train.values[:,mask])
    test = pd.DataFrame(test.values[:,mask])
    feat_num = len(train.iloc[0])
    start = time.time()
    
    end  = time.time()
    print (end - start)
    return BBHA(10,5,m1,m2,train,test) , m1, m2
    
    
def classify(state):
	return getClassification(m1,m2,state)

m1,m2 = create_Ms()
m1 = m1[mask,:]
m2 = m2[mask,:] 
m1 = m1[selection,:]
m2 = m2[selection,:]
m1= np.divide(m1,1013.0)
m2 = np.divide(m2,987.0)
print(m1)
print(m2)
accuracy = "0.958%"
