# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 21:32:37 2016

@author: MAX
"""
# Supervised learning imports

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA

from scipy.stats import expon

def setup_adaboost():
    """
    Creates clf pipeline for AdaBoost
    Returns pipeline and parameters for GridSearchCV
    """

    pipeline =   Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(score_func=f_classif)),
                                 ('clf', AdaBoostClassifier())
                                 ]
                 )
    params = {
              "clf__n_estimators": [20, 25, 30, 40, 50, 100]
             }
    
    return pipeline, params

def setup_logistic():
    """
    Creates clf pipeline for Logistic Regression
    Returns pipeline and parameters for GridSearchCV
    """

    pipeline = Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(score_func=f_classif)),
                                 ('pca', PCA()),
                                 ('clf', LogisticRegression())
                                 ]
                       )
    
    params = {'kbest__k': range(3,30),
              'pca__whiten': (True, False),
#              'clf__C': [ 0.001, 0.1, 10, 10**2, 10**5, 10**10],
              'clf__C': expon(),
              'clf__class_weight': [{False: 1, True: 12},
                                    {False: 1, True: 10},
                                    {False: 1, True: 8},
                                    {False: 1, True: 6},
                                    {False: 1, True: 4}],
              'clf__tol': [2**i for i in range(-20, -1)],
              'clf__penalty': ('l1','l2')
             }
    
    return pipeline, params

def setup_forest():
    """
    Creates clf pipeline for Random Forest Classifier
    Returns pipeline and parameters for GridSearchCV
    """

    pipeline = Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(score_func=f_classif)),
                                 ('clf', RandomForestClassifier())
                              ]
               )
               
    params = {'kbest__k': [4, 9, 20, 'all'],
              "clf__n_estimators": [2, 3, 5, 7],
              "clf__criterion": ('gini', 'entropy'),
              "clf__min_samples_split": [3, 5, 7, 9, 11]
              }   
    
    return pipeline, params

def setup_tree():
    """
    Creates clf pipeline for Decision Tree Classifier
    Returns pipeline and parameters for GridSearchCV
    """

    pipeline = Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(score_func=f_classif)),
                                 ('clf', DecisionTreeClassifier())
                              ]
               )
               
    params = {'kbest__k': [4, 9, 20, 'all'],
              "clf__min_samples_split": [3, 5, 7, 9, 11],
              "clf__criterion": ('gini', 'entropy')
              }  
    
    return pipeline, params
    
def setup_svm():
    """
    Creates clf pipeline for LinarSVC
    Returns pipeline and parameters for GridSearchCV
    """

    pipeline = Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(score_func=f_classif)),
                                 ('clf', LinearSVC())
                              ]
               )
               
    params = {'kbest__k': [4, 9, 20, 'all'],
              'clf__C': expon(),
              'clf__loss': ('hinge', 'squared_hinge'),
              'clf__tol': expon(),
              "clf__class_weight": ['auto']
             }
    
    return pipeline, params