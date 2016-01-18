% Udacity Data Science Project 2 - NYC Subway Data
% Max Edwards
% 10-27-15


# Analyzing the NYC Subway Dataset

## Section 1. Statistical Test
#### 1.1 Which statistical test did you use to analyze the NYC subway data? 

Did you use a one-tail or a two-tail P value? What is the null hypothesis? 
What is your p-critical value?

I used a two tailed Mann-Whitney U test to perform an analysis on NYC \n
subway data. Intuitively, one would think that rain would increase subway \n
riders but we are no evidence to make this hypothesis. Therefore, I used a \n
two-tailed test with the null hypothesis that the two populations are the \n
same (rain does not effect how many people use the subway) and alternative \n
hypothesis that the populations are different (rain does effect how many \n
people use the subway). This test was run using a 95% confidence or \n
p-critical of 0.05. \n

#### 1.2 Why is this statistical test applicable to the dataset? In particular, consider the assumptions that the test is making about the distribution of ridership in the two samples.

The histogram of the hourly entries when it was raining and not raining was
non-normal (see Figure X). Therefore, Welch’s t-test is not appropriate. 
I decided to use a non-parametric test (Mann-Whitney U test) because it 
does not assume the data was drawn from any underlying probability 
distribution.

#### 1.3 What results did you get from this statistical test? These should include the following numerical values: p-values, as well as the means for each of the two samples under test.





~~~~{.python}
def mann_whitney_plus_means(turnstile_weather):
    '''
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the
number of
                entries with rain and the number of entries without
rain
    '''
    df = pandas.read_csv(turnstile_weather)

    with_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] == 1])
    without_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] ==
0])

    x = df['ENTRIESn_hourly'][df['rain'] == 1]
    y = df['ENTRIESn_hourly'][df['rain'] == 0]

    U, p = scipy.stats.mannwhitneyu(x,y)

    return with_rain_mean, without_rain_mean, U, p
~~~~~~~~~~~~~



The results of the above function are as follows:


~~~~{.python}
filename = 'turnstile_data_master_with_weather.csv'
test_results = mann_whitney_plus_means(filename)
print "this is", test_results[1]
~~~~~~~~~~~~~

~~~~{.python}
<type 'exceptions.SyntaxError'>
invalid syntax (chunk, line 4)
~~~~~~~~~~~~~



#### 1.4 What is the significance and interpretation of these results? Based on the p-value of [0.0193], the null hypothesis is rejected and we  can say there is a significant difference between subway ridership when  it is raining and when it is not raining.
