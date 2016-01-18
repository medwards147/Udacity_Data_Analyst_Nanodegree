#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""
from feature_format import featureFormat, targetFeatureSplit


import pickle


enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

# Number of people in dataset - ANS 146
print("The number of people in the dataset: %d" % len(enron_data.keys())) 

# Number of features for an individual (all are the same so I choose one) - ANS 21
print("The number of features for each person are: %d" % len(enron_data['METTS MARK'])) 

# The features provided are
enron_data['METTS MARK'].keys()

# For loop that counts pois - ANS 18
count = 0
for person in enron_data.keys():
    if enron_data[person]["poi"] == 1:
        count += 1
    else:
        continue

print("The number of POI's in the dataset is %d " % count)  

# Count pois in poi_names.txt
poi_yes = 0
poi_total = 0
with open("../final_project/poi_names.txt", "r") as text_file:
    text_file.readline()
    text_file.readline()   
    for line in text_file:

        try:        
            if line[1] == "y":
                poi_yes += 1
                poi_total +=1
            else:
                poi_total +=1
        except:
            continue
    print(poi_yes) # 4
    print(poi_total) # 35
    
# total value of stock of an individual -  James Prentice
#name =  "Prentice James"
name  = "Colwell Wesley"
name = name.upper()
enron_data[name]['from_this_person_to_poi']

name  = "SKILLING JEFFREY K"
enron_data[name]['exercised_stock_options']

#largest total payments of fastow, lay, skilling
names = ["SKILLING JEFFREY K", "FASTOW ANDREW S", "LAY KENNETH L"]
ans = {}
for name in names:
    ans[name] = enron_data[name]['total_payments'] 
print ans

# how many folks in this dataset have a quantified salary or known email?
count_non_nans = 0
count_nans = 0
for key in enron_data.keys():
    if enron_data[key]['salary'] != 'NaN':
        count_non_nans += 1
    else:
        count_nans += 1
print(count_non_nans)
print(count_nans)

# known email?
count_non_nans = 0
count_nans = 0
for key in enron_data.keys():
    if enron_data[key]['email_address'] != 'NaN':
        count_non_nans += 1
    else:
        count_nans += 1
print(count_non_nans)
print(count_nans)

# Percentage of people who have "NaN" as their total payments
count_non_nans = 0
count_nans = 0
for key in enron_data.keys():
    if enron_data[key]['total_payments'] != 'NaN':
        count_non_nans += 1
    else:
        count_nans += 1
print(count_non_nans)
print(count_nans)
print float(count_nans)/(float(count_non_nans) + float(count_nans)) # 14.4%

# Percentage of people who have "NaN" as their total payments
count_non_nans = 0
count_nans = 0
for key in enron_data.keys():
    if enron_data[key]['poi'] == 1:
        if enron_data[key]['total_payments'] != 'NaN':
            count_non_nans += 1
        else:
            count_nans += 1
    else:
        continue
print(count_non_nans)
print(count_nans)
print float(count_nans)/(float(count_non_nans) + float(count_nans)) # 0%

# Percentage of POIs if added 10 POIs with NaN for total_payments
poi_count = 10
count_nans = 0
count_non_nans = 0
for key in enron_data.keys():
    if enron_data[key]['poi'] == 1:
        poi_count += 1
        if enron_data[key]['total_payments'] != 'NaN':
            count_non_nans += 1
        else:
            count_nans += 1
    else:
        continue
print(count_non_nans)
print(count_nans)
print float(count_nans+ 10)/(float(count_non_nans) + float(count_nans + 10)) # 35.7%


# Outlier salary / bonus
for key in enron_data.keys():
    if enron_data[key]['salary'] > 1000000 and enron_data[key]['salary'] != 'NaN':
        print "name: " + key
        print "salary:", enron_data[key]['salary']
        print "bonus: ", enron_data[key]['bonus']
        
# Result ("TOTAL" was really high!) DUH!
       # name: TOTAL
       # salary: 26704229
       # bonus:  97343619

# Checking salary > $1M and bonus > $5M
for key in enron_data.keys():
    if enron_data[key]['salary'] > 1000000 and enron_data[key]['salary'] != 'NaN':
        if enron_data[key]['bonus'] > 5000000 and enron_data[key]['bonus'] != 'NaN':
            print "name: " + key
            print "salary:", enron_data[key]['salary']
            print "bonus: ", enron_data[key]['bonus']

# Checking max and min values for exercised_stock_options
stock_options = {}
for key in enron_data.keys():
    if enron_data[key]['exercised_stock_options'] != 'NaN':
        stock_options[key] = enron_data[key]['exercised_stock_options']
del stock_options['TOTAL']
max(stock_options.iteritems(), key=lambda x:x[1]) # ('LAY KENNETH L', 34348384)
min(stock_options.iteritems(), key=lambda x:x[1]) #('BELFER ROBERT', 3285)

# Checking max and min values for salary
salary = {}
for key in enron_data.keys():
    if enron_data[key]['salary'] != 'NaN':
        salary[key] = enron_data[key]['salary']
del salary['TOTAL']
max(salary.iteritems(), key=lambda x:x[1]) # ('SKILLING JEFFREY K', 1111258)
min(salary.iteritems(), key=lambda x:x[1])  # ('BANNANTINE JAMES M', 477)  

#count 'Nan' per key to see who is missing al ot of data
#found 'THE TRAVEL AGENCY IN THE PARK with 18 NaNs
count_dict = {}
for name in enron_data.keys():
    for value in enron_data[name].values():
        if value == 'NaN':
            count += 1
    count_dict[name] = count
    count = 0    

# Create new feature of ratio of emails from a person to poi compared to total from emails
for name in enron_data.keys():
    from_to_poi_ratio = float(enron_data[name]['from_this_person_to_poi']) / float(enron_data[name]['from_messages'])
    enron_data[name]['from_to_poi_ratio'] = from_to_poi_ratio
    
# Find way to combine finanical features
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
                "total_stock_value",
                #'financial_value' # new feature
                ]
# count of total financial features available for pois            
count_dict = {}
count = 0
for name in enron_data.keys():
    if enron_data[name]['poi'] == 1: 
        for feature in features_financial:    
            if enron_data[name][feature] != 'NaN':
                count += 1   
        count_dict[name] = count
        count = 0

# Percentage of people who have "NaN" as their total payments (POIs only)
count_non_nans = 0
count_nans = 0
for feature in features_financial:
    for key in enron_data.keys():
        if enron_data[key]['poi'] == 1:
            if enron_data[key][feature] != 'NaN':
                count_non_nans += 1
            else:
                count_nans += 1


    #print("for feature " + feature + " the non nan count is {}".format(count_non_nans))
    print(feature + " nan count is {}".format(count_nans))
    
    percentage = float(count_nans)/(float(count_non_nans) + float(count_nans)) # 0%
    #print("for feature " + feature + " the percentage of nans are {}".format(percentage))
    
# Percentage of people who have "NaN" as their total payments
count_non_nans = 0
count_nans = 0
for feature in features_financial:
    for key in enron_data.keys():
        if enron_data[key]['poi'] == 0:
            if enron_data[key][feature] != 'NaN':
                count_non_nans += 1
            else:
                count_nans += 1
        else:
            continue
    #print("for feature " + feature + " the non nan count is {}".format(count_non_nans))
    #print("for feature " + feature + " the nan count is {}".format(count_nans))
    percentage = float(count_nans)/(float(count_non_nans) + float(count_nans)) # 0%
    print("for feature " + feature + " the percentage of nans are {}".format(percentage))
 
# delete 'TOTAL' key prior to visualization data
def deleteKey(data_dict, key):
    del data_dict[key]
    return data_dict
#deleteKey(enron_data, 'TOTAL')

# create plots to aid in feature engineering   
def visualize(data_dict, feature_x, feature_y):
    """ generates a plot of feature y vs feature x, colors poi """
    import matplotlib.pyplot as plt
    data = featureFormat(data_dict, [feature_x, feature_y, 'poi'], remove_all_zeroes=False)

    for datum in data:
        x = datum[0]
        y = datum[1]
        poi = datum[2]
        color = 'blue' if not poi else 'red'
        plt.scatter(x, y, color=color)
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    #plt.show()    
    plt.savefig('../final_project/plots/plot_{0}_{1}'.format(feature_x, feature_y))   # save the figure to file
    plt.close()
    
def visualizeFeatureCombinations():
    from itertools import combinations
    for feature_1, feature_2 in combinations(features_financial, 2):
        visualize(enron_data, feature_1, feature_2)

# Take note of plots where the pois seem to seperate themselves from the rest
# 'total_stock_value', 'exercised_stock_options', 'bonus', 'salary'
# Combination of features to create new 'financial_value' feature
def addFinancialValueFeature(enron_data): 
    financial_value_features = ['total_stock_value', 
                                    'exercised_stock_options', 
                                    'bonus',
                                    'salary']
    for name in enron_data:  
        enron_data[name]['financial_value'] = 0
        for feature in financial_value_features:
            if  enron_data[name][feature] != 'NaN':
                enron_data[name]['financial_value'] += enron_data[name][feature]
    return enron_data
