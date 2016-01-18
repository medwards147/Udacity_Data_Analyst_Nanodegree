# Enron Fraud POI Identifier
Udacity Intro to Machine Learning
Data Analyst Nanodegree Project #5
Max Edwards – 1/16/2016

### Summary and Background
In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives.
The goal of this project is to use data analysis and machine learning techniques to create a model that predicts whether someone is a Person of Interest (POI) based on their financial and email data. The dataset contains a record (or a row) for 146 executives and a field indicating if an individual was a POI in the Enron fraud scandal. Eighteen of these executives were identified as a POI in the actual Enron case and labeled accordingly in the POI field. There are 20 additional fields containing information such as salary, bonus, stock options, emails to, and emails from. Because the data is labeled, the Enron dataset will be used as training data for a supervisory learning algorithm in order to develop a predictive model that attempts to identify if an individual is a POI or not a POI. Theoretically, this model could be used in other financial fraud/scandal scenarios to detect POIs – assuming the same (or similar) features used in the model were available.
Using exploratory data analysis techniques, I was able to identify several issues the dataset.

1.	Outliers.
2.	Useless columns or features.
3.	Useless row or record.

Data exploration is provided in this [ipython notebook](Explore_Enron_Data.ipynb).

### Feature Analysis
Based on what I found during data exploration, I decided to create the feature `poi_email_ratio` which is a ratio of total poi emails over total emails for each person. Additionally, based on the plots I created for the financial features, I decided to add together the values for `total_stock_value`, `bonus`, and `salary`. I felt this could be a powerful feature as will effectively multiply the differences I was seeing between POIs and non-POIs in the plots. Finally, I decided to square and take the log of all the financial features to get features' high-order and interaction terms. 
After adding in the additional features, there were 50 total features. Using SelectKBest, the final model chosen uses k=27 the features. The top 10 features that ended up being used in the final model are provided in the table below with the importance values.

| Feature       | SelectKBest Best Importance |
| --------------------------- |:-------------:|
| 'financial_value' | 29.025
| 'square_exercised_stock_options' | 26.033
| 'exercised_stock_options' | 24.815
| 'total_stock_value' | 24.183
| 'square_total_stock_value'| 20.839
| 'bonus' | 20.792
| 'salary'| 18.290
| 'log_other'| 16.540
| 'log_expenses'| 13.895
| 'square_salary'| 13.581

This pipeline included a scaler (MinMaxScaler) prior to finding the best parameters. I choose to do this so each feature was weighted equally (especially since I had squared and log features included). I choose a range of 3 to 30 for `k` to be fed into RandomizedSearchCV. I originally a smaller discrete range but using RandomizedSearchCV allows for me to put a big range without any computation issues (as I would get with GridSearchCV). Additionally, I decided to use Principal Component Analysis (PCA) to reduce the dimensionality of the features chosen by SelectKBest for my chosen model. This further reduces the feature count used in the model without losing much of the information from the larger set of features.

### Algorithm Chosen and Performance
I created the following 5 separate supervised learning models to predict a `poi`:

1. AdaBoost
2. Logistic Regression
3. Random Forest
4. Decision Tree Classifier
5. Linear Support Vector Machine

I used a pipeline to scale, select features, and create an estimator object. Then, I used RandomizedSearchCV with a StatifiedShuffleSplit cross validation method. The model parameters and pipeline can be viewed in python script [models.py](models.py).

The algorithm chosen was a Logistic Regression as the recall was the best (0.7985) while still maintaining relatively good precision (above 0.3000). Linear SVM performed very similarly with a good recall but was less precise. Adaboost and Random Forest both had less than 0.3 recalls but had highest accuracies > 0.80 due to better precision. Decision Tree had the best accuracy with the 3rd best recall and best precision. See the Evaluation Metrics section for the detailed metrics and the reason for why recall was chosen as the most important metric.

### Algorithm Parameter Tuning
Tuning algorithm parameters is the process of changing variables that dictate how the algorithm interacts with the data to generate a prediction in order to optimize the model for what you are trying to predict. If you don't do this well, the supervised learning model you develop will either be too biased (underfit) or have too much variance (overfit). In the case of too much bias, your model will perform well on the training data and generally worse on out of sample data. In the case of too much variance, your model will perform very well on training data but perform poorly on out of sample data.

For the Enron case, I tuned the parameters of the models by using hyperparameter optimization methods. This means a discrete or continuous range of values for a parameter is provided and the model is fit to each combination of parameters. The best set of parameters is chosen based on the best score for the metric you are trying to optimize. For most of my models, I was using the f1-score metric to optimize. For the Logistic Regression model, in order to achieve above a 0.30 precision, I choose to optimize precision. In general, this is just something else I had to tweak depending on what results I was seeing when evaluating a model.

Using scikit learn, GridSearchCV will perform an exhaustive search over the specified parameter values for an estimator. However, I choose to use RandomizedSearchCV to control the number of iterations in order to avoid extremely expensive computations if too many parameter combinations are set. Even though RandomizedSearchCV tested out several combinations of parameters, I still needed to tweak the parameter ranges for each model. This was somewhat easy and I could provide a large range of parameters and run RandomizedSearchCV several times to find the best combination.  In the case of the Logistic Regression model (my chosen algorithm), I found that I can set the `C` to an exponential distribution rather than a discrete range of values and used a list comprehension on `tol` to achieve a good parameter range.

### Validation
Validation is testing how a model will generalize to an independent data set. If you don't perform cross-validation, you can overfit your model resulting in good performance on your training data but poor performance with out of sample data. I used StatifiedShuffleSplit cross validation to create a 100 difference datasets with a test size of 10% to find the best model. 

### Evaluation Metrics
The following table provides a breakdown of the performance for each model. The main metric I was interested in was Recall as this is the amount of times the model predicted a poi when it was actually a poi. This is good because it means you are less likely to miss a poi when you have a higher recall. I think for the purpose of the Enron, you'd be better off identifying a possible poi then investigating the person rather than missing a poi. If the investigation results in the person is not a poi, as they say, "no harm no foul". The secondary metric used to evaluate the model was precision.  It is important to keep in mind precision as the it takes into account how many times you incorrectly classify someone as a poi. If you can improve on precision without harming recall too much, then it is worth it. However, in the case of Enron, I believe maximizing recall while keeping precision above a satisfactory threshold is the best tactic. Balancing these is something that could be tuned depending on what the user actually want.

| Model | F1-score | Recall | Precision | Accuracy |
| --------------------- |:------:|:----:|:-----:|:-----:|
| AdaBoost     			| 0.32907 | 0.28950	| 0.38117 | 0.84260 |
| Logistic Regression   | 0.45158 | 0.79850 | 0.31480 | 0.74140 |
| Random Forest 		| 0.30143 | 0.25750 | 0.36344 | 0.84087 |
| Decision Tree			| 0.50313 |	0.48300	| 0.52500 | 0.87280 |
| Linear SVM 			| 0.38099 |	0.70150	| 0.26151 | 0.69607 |
Therefore, I choose the Logistic Regression model with the following parameters as it achieved the best Recall while still meeting the required 0.3 threshold for precision. Note: this provides the pipeline used which includes scaling, kbest, and pca prior to the logistic regression estimator.
`Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), ('kbest', SelectKBest(k=27, score_func=<function f_classif at 0x000000001BE56278>)), ('pca', PCA(copy=True, n_components=None, whiten=False)), ('clf', LogisticRegression(C=0.444273370205, class_weight={False: 1, True: 6},
          dual=False, fit_intercept=True, intercept_scaling=1,
          max_iter=100, multi_class='ovr', penalty='l1', random_state=None,
          solver='liblinear', tol=0.03125, verbose=0))])`
