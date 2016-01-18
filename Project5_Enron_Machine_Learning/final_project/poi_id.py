#!/usr/bin/python

import pickle
import sys
sys.path.append("../tools/")

import numpy as np
import math
import pprint as pp

from feature_format import featureFormat, targetFeatureSplit
from tester import test_classifier, dump_classifier_and_data
from models import setup_adaboost, setup_logistic, setup_forest, setup_tree, setup_svm

#from sklearn.grid_search import GridSearchCV
from sklearn.grid_search import RandomizedSearchCV
from sklearn.cross_validation import train_test_split, StratifiedShuffleSplit
from sklearn.pipeline import Pipeline

from sklearn.metrics import make_scorer
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix

from sklearn.feature_selection import SelectKBest
from sklearn.decomposition import PCA

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

#from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler


def define_features():
    # binary indicating if poi or not
    poi = ["poi"]
    
    # Email features provided in enron dataset
    features_email = [
                    #"email_address", # This is unique to the individual
                    "from_messages",
                    "from_poi_to_this_person",
                    "from_this_person_to_poi",
                    "shared_receipt_with_poi",
                    "to_messages"
                    ]
    
    # Financial features provided in enron dataset
    features_financial = [
                    "bonus",
                    "deferral_payments",
                    "deferred_income",
                    "director_fees",
                    "exercised_stock_options",
                    "expenses",
                    "loan_advances",
                    "long_term_incentive",
                    "other",
                    "restricted_stock",
                    "restricted_stock_deferred",
                    "salary",
                    "total_payments",
                    "total_stock_value"
                    ]
    return poi, features_email, features_financial  

def load_data():
    """
    Generates scatter plot and colors set to identify pois 
    """

    # load enron data from pickle file
    enron_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

    # Removing outliers
    keys_remove = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
    for key in keys_remove:
        del enron_dict[key]

    return enron_dict

def add_new_features(enron_dict, features_list):
    """
    Adds new email and financial related features
    """
    
    ### New email related features ###
    
    for name in enron_dict.keys():

        # Add ratio of POI messages to total.
        try:
            email_count = enron_dict[name]['from_messages'] + enron_dict[name]['to_messages']
            poi_email_count = enron_dict[name]["from_poi_to_this_person"] +\
                                    enron_dict[name]["from_this_person_to_poi"]
            poi_email_ratio = float(email_count) / float(poi_email_count)
            enron_dict[name]['poi_email_ratio'] = poi_email_ratio
        except:
            enron_dict[name]['poi_email_ratio'] = 'NaN'
    
    ### New financial related features ###
    
    # list of features found during exploration that where poi's were visibly
    # seperated from non-pois
    financial_value_features = ['total_stock_value', 
                                'bonus',
                                'salary']
    
    # loops through each name and adds together the values of financial_value_features                            
    for name in enron_dict.keys():   
        enron_dict[name]['financial_value'] = 0
        for feature in financial_value_features:
            if  enron_dict[name][feature] != 'NaN':
                enron_dict[name]['financial_value'] += enron_dict[name][feature] 

    new_features = ['poi_email_ratio', 'financial_value']
    
    
    # add squared features and log of square features 
    for name in enron_dict:
        for feature in features_list:        
            try:
                enron_dict[name]['square_{}'.format(feature)] = math.pow(enron_dict[name][feature], 2)
            except:
                enron_dict[name]['square_{}'.format(feature)] = 'NaN'
        for feature in features_list:
            try:
                enron_dict[name]['log_{}'.format(feature)] = math.log10(enron_dict[name]['square_{}'.format(feature)])
            except:
                enron_dict[name]['log_{}'.format(feature)] = 'NaN'
                
    # create new_features list. I choose a name I knew is in the dictionary.
    # bad form to hard code the name but I'm still learning!
    for feature in enron_dict['METTS MARK']:
        if feature.startswith("square") or feature.startswith("log"):
            new_features.append(feature)     
    
    return enron_dict, new_features

def feature_scale(features, scale_type='minmax'):
    """
    Scales features based on chosen scaler
    """
    if scale_type=='minmax':
        scaler = MinMaxScaler()
    elif scale_type=='standard':
        from sklearn.preprocessing import StandardScaler       
        scaler = StandardScaler()
    else:
        print("Invalid scale_type")
   
    scaled_features = scaler.fit_transform(features)    
    return scaled_features

def find_k_best(features_list, features, labels, k=10, scale=True):
    """
    Reports features...
    """
    # scale features prior to SelectKBest
    if scale:    
        features = feature_scale(features)
    
    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    #k_best_features = dict(sorted_pairs[:k])
    pp.pprint(sorted_pairs)
    return sorted_pairs      

def fit_model(model='logistic', scoring=5, cv=None, n_iter=10):
    """
    Creates pipeline and fits using RandomizedSearchCV for a user chosen model
    cross validation type, scoring, and randomized parameter search iterations
    """
    
    if model == 'logistic':    
        pipe, params = setup_logistic()
        print("Fitting Logistic Regression...")        
    elif model == 'forest':
        pipe, params = setup_forest()
        print("Fitting Random Forest...")
    elif model == 'tree':
        pipe, params = setup_tree()
        print("Fitting Tree...")
    elif model == 'adaboost':
        pipe, params = setup_adaboost()
        print("Fitting AdaBoost...")
    elif model == 'svm':
        pipe, params = setup_svm()
        print("Fitting SVM...")        
    
    clf = RandomizedSearchCV(pipe, params, scoring=scoring, cv=cv, n_iter = n_iter).fit(features, labels)
    
    return clf

# Evaluation
def evaluate_model(clf, features, labels, metric='metrics'):
    """
    Predicts and evaluates a fitted model
    """
    
    # Split data into training and test sets
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=.5)

    predictions = clf.predict(features_test)
    
    # useful metrics  
    if metric == 'metrics':
        f1 = f1_score(labels_test, predictions)
        recall = recall_score(labels_test, predictions)
        precision = precision_score(labels_test, predictions)
        #roc = roc_auc_score(labels_test, predictions)
        print("f1-score: {}".format(f1))
        print("recall: {}".format(recall))
        print("precision: {}".format(precision))  
        #print("roc: {}".format(roc))        
        return f1, recall, precision
    # confusion matrix    
    elif metric == 'conf_matrix':
        conf_matrix = confusion_matrix(labels_test, predictions)
        print conf_matrix
        return conf_matrix

    else:
        return None
    
    return None

        
if __name__ == '__main__':
    
    # create initial features list
    poi, features_email, features_financial = define_features()
    initial_features = poi + features_email + features_financial # 20 features
    
    # Load the data and prep the data
    enron_dict = load_data()
    
    # add new features to enron_dict
    enron_dict, new_features = add_new_features(enron_dict, features_financial) # adds 2 features
    
    # final features list (initial + new)
    # initial_features must be first as 'poi' needs to be first in list
    features_list = initial_features + new_features     
    
    # Store to my_dataset for easy export below
    my_dataset = enron_dict
    
    # Extract features and labels from dataset for local testing
    data = featureFormat(my_dataset, features_list, sort_keys = True)
    
    # Split into labels and features ('poi' must be first col in the data)
    labels, features = targetFeatureSplit(data)

    # Count of features
    feature_count = np.array(features).shape[1] 
    
    # K best features
    #find_k_best(features_list, features, labels, k=10, scale=True)

    # setup scoring and cross validation objects for GridSearchCV
    scoring = make_scorer(precision_score)   
#    scoring = make_scorer(recall_score)    
    #The folds are made by preserving the percentage of samples for each class.    
    shuffle = StratifiedShuffleSplit(labels, n_iter=100, test_size=0.1)    
    
    # number of iterations to run for RandomizedSearchCV   
    # model. Could write in error handler but for now I'm more worried about
    # tuning the models.
    num_iter_random = 75
    
    # Models to choose from
    models = ['logistic', 'forest', 'tree', 'adaboost', 'svm']
    ####### Fit Models ##############
    # NEED TO CHANGE num_iter_random depending on model
    # Uncomment to fit a chosen model based on above list index
    # clf = fit_model(model=models[0],
    #                               scoring=scoring, 
    #                               cv=shuffle, 
    #                               n_iter=num_iter_random)
    #
    # best_pipe = clf.best_estimator_
    #################################
    
    ###### Evaluate models ##########
    # take average of 10 runs... could do function but this works
    # f1_list = []
    # recall_list = []
    # precision_list = []    
    # for i in range(10):    
    #    f1, recall, precision = evaluate_model(clf, features, labels, metric='metrics')
    #    f1_list.append(f1)
    #    recall_list.append(recall)
    #    precision_list.append(precision)
    ################################

    ###### BEST PARAMS FOUND #######  
    # adaboost best params
    # {'clf__n_estimators': 30}
    #
    # Tree best params
    #  {'clf__criterion': 'entropy', 'kbest__k': 4, 'clf__min_samples_split': 7}
    #
    # Logistic regression best params
    # {'clf__C': 0.4442733702050227, 'pca__whiten': False, 'kbest__k': 27, 'clf__penalty': 'l1', 'clf__tol': 0.03125, 'clf__class_weight': {False: 1, True: 6}}
    # Forest best params
    # {'clf__criterion': 'gini', 'kbest__k': 9, 'clf__n_estimators': 3, 'clf__min_samples_split': 7}    
    #
    # Linear SVM
    # {'clf__tol': 0.10549452845523806, 'kbest__k': 9, 'clf__loss': 'squared_hinge', 'clf__C': 2.2813756362277777, 'clf__class_weight': 'auto'}    
    #################################
    
    # Manually run best model found for project data dump
    clf_best = Pipeline(steps=[('scaler', MinMaxScaler()),
                                 ('kbest', SelectKBest(k=27)),
                                 ('pca', PCA(whiten=False)),
                                 ('clf', LogisticRegression(C=0.4442733702050227, tol=0.03125, class_weight={False: 1, True: 6}, penalty='l1'))
                              ]
               )
     # Used to find the K best features for the chosen model
     # k_best_features = find_k_best(features_list, features, labels, k=27, scale=True)
    
    clf_best = clf_best.fit(features, labels)
   
    # Test - do this at end once I find my best after evaluation
    test_classifier(clf_best, my_dataset, features_list)
    
    # Dump classifier for grading - change to the clf that you found best results
    dump_classifier_and_data(clf_best, my_dataset, features_list)