# Analyzing the NYC Subway Dataset
Max Edwards
Data Analyst Nanodegree Project#3, 10-30-15

## Section 1. Statistical Test

### 1.1 Which statistical test did you use to analyze the NYC subway data? Did you use a one-tail or a two-tail P value? What is the null hypothesis? What is your p-critical value?

I used a two tailed Mann-Whitney U test to perform an analysis on NYC subway data. Intuitively, one would think that rain would increase subway riders but we have no evidence to make this hypothesis. Therefore, I used a two-tailed test with the null hypothesis that the two populations are the same and an alternative hypothesis that the populations are not the same. This test was run using a 95% confidence or p-critical of 0.05.

### 1.2 Why is this statistical test applicable to the dataset? In particular, consider the assumptions that the test is making about the distribution of ridership in the two samples

The histogram (see Section 3) of the hourly entries when it was raining and not raining was non-normal. Therefore, Welch’s t-test is not appropriate. I decided to use a non-parametric test (Mann-Whitney U test) because it does not assume the data was drawn from any underlying probability distribution.

### 1.3 What results did you get from this statistical test? These should include the following numerical values: p-values, as well as the means for each of the two samples under test.

I ran the following code to obtain the results from performing a Mann-Whitney U test.

`turnstile_weather = 'turnstile_data_master_with_weather.csv'`

`df = pandas.read_csv(turnstile_weather)`

`with_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] == 1])`

`without_rain_mean = np.mean(df['ENTRIESn_hourly'][df['rain'] == 0])`

`x = df['ENTRIESn_hourly'][df['rain'] == 1]`

`y = df['ENTRIESn_hourly'][df['rain'] == 0]`

`U, p = scipy.stats.mannwhitneyu(x,y)`

`U = U*2 # for two tail`

`p = p*2 # for two tail`

`print with_rain_mean`

`print without_rain_mean`

`print U`

`print p`

Output of code I wrote is below. Note: I tried to update my scipy package but that did not seem to change my results. Previous grader suggested I should be receiving a p-value of ~0.25:

`Mean ridership when it is raining is and 1,105.44637675`

`Mean ridership when it is not raining is and 1,090.27878015`

`U stat is and 3,848,818,334.0`

`p-value is and 0.038619268827585131`

### 1.4 What is the significance and interpretation of these results?

## Section 2. Linear Regression

### 2.1 What approach did you use to compute the coefficients theta and produce prediction for ENTRIESn_hourly in your regression model:

### 2.2 What features (input variables) did you use in your model? Did you use any dummy variables as part of your features?

### 2.3 Why did you select these features in your model?

### 2.4 What are the parameters (also known as "coefficients" or "weights") of the non-dummy features in your linear regression model?

### 2.5 What is your model’s R2 (coefficients of determination) value?

### 2.6 What does this R2 value mean for the goodness of fit for your regression model? Do you think this linear model to predict ridership is appropriate for this dataset, given this R2 value?

## Section 3. Visualization

## Section 4. Conclusion

## Section 5. Reflection

The main issue I noticed from the start was that the entries and exits did not lineup (mean of 1095.35 entries versus mean of 886.89 exits). This is concerning from a data integrity standpoint as there is somewhat of a significant difference between the two variables. Also, the thunder variable is all zeros so it seems the column was added but the data was never actually recorded. I would dig further given these initial findings to determine if I would actually use this dataset in real world applications.
The SGD regression model was sufficient for the purposes of this class and being able to make a decent prediction of subway ridership. It is certainly not anywhere close to a model that could actually be used for a production type environment. By introducing a linear model, you are inherently introducing bias – meaning the model lacks the ability to account for a lot of the variation (hence the difficulty of raising the R-squared). Additionally, it is usually better to split up the available data into a training set, cross-validation set, and test set in order to create an environment where you can test the model out of sample. This would become more important when using the more complicated models.
The Mann-Whitney U test was used to understand if there was a significant difference between ridership when it’s raining versus not raining. By using this test, we are limiting ourselves in terms of what we can quantitatively say
about the actual difference between the two populations. We provide the mean and median but we don’t have any information regarding the variance.

## References

1. http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
2. http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor
3. https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test
4. http://matplotlib.org/users/pyplot_tutorial.html