import numpy as np 
import json, pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# NOTE: Make sure that the class is labeled 'target' in the data file
g=json.load(open('speech_silence_tpotclassifier_.json'))
tpot_data=g['labels']
features=g['data']

training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data, random_state=None)

# Average CV score on the training set was:0.9527629233511586
exported_pipeline = LinearSVC(C=15.0, dual=False, loss="squared_hinge", penalty="l2", tol=0.001)

exported_pipeline.fit(training_features, training_target)
print('saving classifier to disk')
f=open('speech_silence_tpotclassifier.pickle','wb')
pickle.dump(exported_pipeline,f)
f.close()
