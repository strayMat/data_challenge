# coding: utf-8

import numpy as np
import pandas as pd
import pylab as plt
from time import sleep
from IPython import display
import math

### Fetch the data and load it in pandas
data = pd.read_csv('train.csv')
print ("Size of the data: ", data.shape)

#%%
# See data (five rows) using pandas tools
print (data.head())

# get the (somewhat rare) columns of interest
#col1 = data['DATE']
#col2 = data['DAY_WE_DS']
#col3 = data['TPER_HOUR']
#newdata=[col1,col2,col3]

#df = pd.DataFrame (data = newdata)
#df = df.T
#df.to_csv("train.csv", sep=',')


### Prepare input to scikit and train and test cut

#binary_data = data[np.logical_or(data['Cover_Type'] == 1,data['Cover_Type'] == 2)] # two-class classification set
X = data.drop('N_Call', axis=1)
#X = X.drop('DAY_WE_DS', axis=1)
X = X.drop('DATE', axis=1).values

y = data['N_Call'].values
print (np.unique(y))
#y = 2 * y - 3 # converting labels from [1,2] to [-1,1]

#%%
# Import cross validation tools from scikit
from sklearn.cross_validation import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=None)


#%%
### Train a single decision tree

from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(max_depth=8)

# Train the classifier and print training time
clf.fit(X_train, y_train)

#%%
# Do classification on the test dataset and print classification results
from sklearn.metrics import classification_report
target_names = data['N_Call'].unique().astype(str).sort()
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred, target_names=target_names))

#%%
# Compute accuracy of the classifier (correctly classified instances)
from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)
#print(as)



#===================================================================
#%%
### Train AdaBoost

# Your first exercise is to program AdaBoost.
# You can call *DecisionTreeClassifier* as above, 
# but you have to figure out how to pass the weight vector (for weighted classification) 
# to the *fit* function using the help pages of scikit-learn. At the end of 
# the loop, compute the training and test errors so the last section of the code can 
# plot the lerning curves. 
# 
# Once the code is finished, play around with the hyperparameters (D and T), 
# and try to understand what is happening.

D = 2 # tree depth
T = 500 # number of trees
w = np.ones(X_train.shape[0]) / X_train.shape[0]
training_scores = np.zeros(X_train.shape[0])
test_scores = np.zeros(X_test.shape[0])

Yt = np.zeros(X_train.shape[0])
Ytp = np.zeros(X_train.shape[0])

Yttest = np.zeros(X_test.shape[0])
Ytptest = np.zeros(X_test.shape[0])

ts = plt.arange(len(training_scores))
training_errors = []
test_errors = []

#===============================
for t in range(T):
    
    # Your code should go here
    
    clf = DecisionTreeClassifier(max_depth=D)
    clf.fit(X_train, y_train, w)
    yt = clf.predict(X_train)
    
    #I = np.where (yt != y_train)
    #temp = np.where (yt != y_train,y_train, w)
    num = 0
    
    for i in range (X_train.shape[0]):
        if (yt[i] != y_train[i]):
            num+=w[i]
    
    
    #J = np.ones(X_train.shape[0])
    #num = np.sum(temp)
    denom = np.sum(w)
    
    gammat = num/denom

    #print(gammat)    
    
    alphat = math.log((1-gammat)/gammat)
    for i in range (X_train.shape[0]):
        w[i] = w[i] * math.exp(alphat*(yt[i] != y_train[i]))
    
    
    yttest = clf.predict(X_test)
    
    Yt += alphat * yt
    Yttest += alphat *yttest
    #print(Yt)
    
    for i in range (X_train.shape[0]):
        Ytp[i]=math.floor(Yt[i])
    
    for i in range (X_test.shape[0]):
        Ytptest[i]=math.floor(Yttest[i])    
    
    tre = 0
    for i in range (X_train.shape[0]):
        tre += (Ytp[i] != y_train[i])
        
    
    
    tee = 0
    for i in range (X_test.shape[0]):
        tee += (Ytptest[i] != y_test[i])
    
    training_errors.append(tre)
    test_errors.append(tee)


plt.plot(training_errors, label="training error")
plt.plot(test_errors, label="test error")
plt.legend()