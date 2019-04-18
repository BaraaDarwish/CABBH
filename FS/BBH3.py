import math
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
import random
from datetime import datetime
X = pd.DataFrame()
y = pd.DataFrame()
feat_num = 0
random.seed(datetime.now)

class Star:
    
    def __init__(self):
      self.criteria =  (random.uniform(0.1,0.9))  
      self.selection = selection_init()
      self.fitness = accuracy_random_forest(self.selection , self.criteria)
    
    def set_fitness(self, fit):
        self.fitness = fit
    def get_fitness(self):
        return self.fitness
    def get_star(self , index):
        return self.index(index)
      

#choosing the selection of features
def selection_init ():
        
        arr = []
        for i in range (feat_num):
            arr.append(random.random())

        return arr

#creating the stars
def stars_init_(stars_num):
    starts_array = []
    for i in range(stars_num):
        starts_array.append(Star())
        


#converts the float variables in the selection array to binary array
def mask_converter(selection , criteria):
        binary_arr = []

        for i in selection:
            if(i > criteria):
                binary_arr.append(True)
            else:
                binary_arr.append(False)
        return binary_arr




#calculating fitness using 10 fold cv random forest
def accuracy_random_forest(selection_arr , criteria):

    binary = mask_converter(selection_arr , criteria)
    mask = np.array(binary)
    X_masked = X.values[:, mask]
    print('the number of selected features :')
    print( len(X_masked[3]))
    forest = RandomForestClassifier( random_state = 1 ,n_estimators= 10)
    kfold = KFold(5 , shuffle = False)
    accu_arr = []

    for train_index, test_index in kfold.split(X_masked):    
        X_train, X_test = X_masked[train_index], X_masked[test_index]
        y_train, y_test = y[train_index], y[test_index]

        
        forest.fit(X_train,y_train)
        sc = forest.score(X_test,y_test)
        accu_arr.append(sc)
        #print("accuracy is ",sc)
    print('the mean accuracy = %s' % np.mean(accu_arr))
    return np.mean(accu_arr)

#choosing the max fitness
def max_fitness(stars):
    max_fit = stars[0].get_fitness()
    max_index = 0
    for star in stars:
        if max_fit < star.get_fitness():
            max_fit = star.get_fitness()
            max_index = stars.index(star)
    print("maximum fitness = " , max_fit)

    return max_index



#returs the number of features in a given star
def feature_count(star):
    count = 0
    for i in star.selection:
        if i > star.criteria:
            count += 1
    return count




#calculates the event horizon
def radius(bh_index, stars):
    _sum = 0.0
    for s in stars:
        if stars.index(s) != bh_index:  # is bh included ??
            _sum += s.get_fitness()
    return stars[bh_index].get_fitness()/_sum



#the main function ***
def BBHA(stars_num, iterations_number, rand):
    # #create stars#
    list_of_stars = []

    for i in range(stars_num):
        star = Star()
        list_of_stars.append(star)


    bh_index = max_fitness(list_of_stars)

    iterations = 0

    #black_hole: Star = copy.copy(list_of_stars[bh_index])
    print ("black hole is the star num" , bh_index)

    # ***** the begining of the loop *********
    while iterations < iterations_number:

        for a in list_of_stars:
            tries = 0
            next_ = False
            #old_fitness = a.get_fitness()
           
            while(next_ == False):
               
                print("Star Num" , list_of_stars.index(a))
                a.set_fitness(accuracy_random_forest(a.selection , a.criteria))
                if a.get_fitness() > list_of_stars[bh_index].get_fitness():
                          
                          bh_index = list_of_stars.index(a)
                          
                          
                          # remove if not used
                elif a.fitness == list_of_stars[bh_index].fitness and feature_count(list_of_stars[bh_index]) > feature_count(a):
                              
                              bh_index = list_of_stars.index(a)
                              #a.fitness = old_fitness
                _r = radius(bh_index, list_of_stars)
                print ("black hole is the star num" , bh_index , "with fitness" , list_of_stars[bh_index].get_fitness())
                if  math.sqrt(math.pow((list_of_stars[bh_index].fitness - a.fitness), 2)) < _r or tries>=10 :
                                  next_ = True
                                  
                if list_of_stars.index(a) != bh_index:
                    
                    for i  in range (len(a.selection)):
                    
                         a.selection[i] = a.selection[i] + (rand * (list_of_stars[bh_index].selection[i] - a.selection[i]))
                         if abs(math.tanh(a.selection[i])) > 0.5:
                                  a.selection[i] = 1
                         else:
                                  a.selection[i] = 0
                tries +=1
        iterations += 1
    print("the number of features selected: ")
    print(feature_count(list_of_stars[bh_index]))
    binary = mask_converter(list_of_stars[bh_index].selection , list_of_stars[bh_index].criteria)
    mask = np.array(binary)
    X_masked = X.values[:, mask]
    new_ds = pd.DataFrame(np.c_[X_masked, y])
    return  feature_count(list_of_stars[bh_index]) , accuracy_random_forest(list_of_stars[bh_index].selection , list_of_stars[bh_index].criteria),new_ds.to_csv()

def old_fitness(x, y ):
   
    
    forest = RandomForestClassifier( random_state = 1 ,n_estimators= 10)
    kfold = KFold(5 , shuffle = False)
    accu_arr = []
    #for train_index, test_index in kfold.split(X_masked):
    for train_index, test_index in kfold.split(X):    
        X_train, X_test = x.values[train_index], x.values[test_index]
        y_train, y_test = y[train_index], y[test_index]
     
        
        forest.fit(X_train,y_train)
        sc = forest.score(X_test,y_test)
        accu_arr.append(sc)
        #print("accuracy is ",sc)
    print('the mean accuracy = %s' % np.mean(accu_arr))
    return np.mean(accu_arr)

def FS(csv , stars_num = 10 , iterations_number=10):
    data = pd.read_csv(csv)
    global X
    X = data[data.columns[:-1]]
    global y
    global  feat_num
   
    y = data[data.columns[-1]]
    feat_num = len(X.iloc[0])
    random.seed(datetime.now)
    old_accuracy = old_fitness(X,y)
    new_features ,new_accuracy , new_ds = BBHA(stars_num,iterations_number, 0.5  )
    return old_accuracy , feat_num , new_accuracy, new_features , new_ds


