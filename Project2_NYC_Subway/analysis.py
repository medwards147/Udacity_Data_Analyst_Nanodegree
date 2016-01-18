# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 20:35:39 2015

@author: MAX
"""

from ggplot import *
import pandas
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.stats
from sklearn.linear_model import SGDRegressor


def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histogram may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''

    df = pandas.read_csv(turnstile_weather)

    plt.figure()

    df['ENTRIESn_hourly'][df['rain'] == 0].hist(alpha = 0.5) # historgram for hourly entries when it is raining
    df['ENTRIESn_hourly'][df['rain'] == 1].hist(alpha = 0.5) # historgram for hourly entries when it is not raining

    plt.suptitle('Histogram of Entries Hourly')
    plt.xlabel('Entries Hourly')
    plt.ylabel('Frequency')
    plt.legend(['No Rain', 'Rain'])

    return plt

def day_of_week_plot(turnstile_weather):
    
    # data frame using turnstile weather_data. Formatting date column to use dayofweek method
    df = pandas.read_csv(turnstile_weather)
    df['DATEn_formatted'] = pandas.to_datetime(df['DATEn'], format='%Y-%m-%d')
    df['dayofweek'] = df['DATEn_formatted'].apply(lambda x: x.dayofweek)
    
    # group data using groupby function and aggregate method
    grouped = df.groupby(['dayofweek'], as_index=False).aggregate(np.mean)
    
    # create plot to show average entries by each day of week
    plot = ggplot(aes('dayofweek', 'ENTRIESn_hourly'), grouped) + \
    geom_point(color = 'black') +geom_line(color = 'red') + \
    ggtitle("NYC Subway Riders by Day of Week") + \
    xlab("Day of Week (0 = Monday, 6 = Sunday)")
    
    return plot    

def mann_whitney_plus_means(turnstile_weather):
    '''
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    '''
    df = pandas.read_csv(turnstile_weather)
    
    with_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] == 1])
    without_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] == 0])
        
    x = df['ENTRIESn_hourly'][df['rain'] == 1]
    y = df['ENTRIESn_hourly'][df['rain'] == 0]
    
    U, p = scipy.stats.mannwhitneyu(x,y)
    
    return with_rain_mean, without_rain_mean, U, p


def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    ''' 
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    ''' 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. Takes the means and standard deviations of the original
    features, along with the intercept and parameters computed using the normalized
    features, and returns the intercept and parameters that correspond to the original
    features.
    ''' 
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    ### YOUR CODE GOES HERE ###
    
    model = SGDRegressor().fit(features,values)
    #model.fit(features, values)
    intercept = model.intercept_
    params = model.coef_
    
    return intercept, params

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.40 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subset (~50%) of the data contained in 
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with 
    this exercise on your own computer, locally.
    
    If you receive a "server has encountered an error" message, that means you are 
    hitting the 30-second limit that's placed on running your program. Try using a
    smaller number of features or fewer iterations.
    '''
    ################################ MODIFY THIS SECTION #####################################
    # Select features. You should modify this section to try different features!             #
    # We've selected rain, precipi, Hour, meantempi, and UNIT (as a dummy) to start you off. #
    # See this page for more info about dummy variables:                                     #
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.get_dummies.html          #
    ##########################################################################################
    features = dataframe[['rain', 'precipi', 'Hour', 'meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    
    # Get numpy arrays
    features_array = features.values
    values_array = values.values
    
    means, std_devs, normalized_features_array = normalize_features(features_array)

    # Perform gradient descent
    norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
    
    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    
    predictions = intercept + np.dot(features_array, params)
    # The following line would be equivalent:
    # predictions = norm_intercept + np.dot(normalized_features_array, norm_params)
    
    return predictions    
    
if __name__ == '__main__':
    filename = 'turnstile_data_master_with_weather.csv'
    print entries_histogram(filename)
    print day_of_week_plot(filename)
    print mann_whitney_plus_means(filename)
    test_results = mann_whitney_plus_means(filename)
    print "this is", test_results[1]
    
   # linear_regression()

    
    