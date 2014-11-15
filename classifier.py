from sklearn.linear_model import SGDClassifier
from sklearn import svm
import numpy as np
import csv

np.set_printoptions(threshold=np.nan)

stringshowdata = []
showratings = []

#turn the huge binarized tropelist string into a proper array
def parsestringarrayAsarray(stringarray):
    array = []
    temparray = stringarray.split(', ')
    for i in range(0,len(temparray)):
        if '[' in temparray[i]:
            fixd = temparray[i][1]
            array += [int(fixd)]
        elif ']' in temparray[i]:
            fixd = temparray[i][0]
            array += [int(fixd)]
        else:
            array += [int(temparray[i])]
    return array

#extract all tropelist and rating data from masterarraylist
with open('masterarraylist.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        stringshowdata += [row[1]]
        showratings += [int(row[2])] #cast as int or float depending on what classifier is used. int for SGD, float for SVM
    f.close()

showdata = []
for show in stringshowdata:
    showdata += [parsestringarrayAsarray(show)]

#Stochasic Gradient Descent Stuff only for discrete integer classification ie genre classification. can be used for "continuous" ratings if all Y/showratings is on a scale of 0 to 10000
clf = SGDClassifier(alpha=0.0001, class_weight=None, epsilon=0.1, eta0=0.0, fit_intercept=True, l1_ratio=0.15, learning_rate='optimal', loss='hinge', n_iter=5, n_jobs=1, penalty='l2', power_t=0.5, random_state=None, shuffle=False, verbose=0, warm_start=False)

clf.fit(showdata, showratings)
print clf.coef_
#print clf.predict()


#Support Vector Machines stuff for floatingpoint movie ratings
# clf = svm.SVR(kernel='rbf', degree=3, gamma=0.0, coef0=0.0, tol=0.001, C=1.0, epsilon=0.1, shrinking=True, probability=False, cache_size=200, verbose=False, max_iter=-1, random_state=None)

# clf.fit(showdata, showratings)
# print clf.score(showdata,showratings)
# print clf.predict()
