
### Analyzing the NYC Subway Dataset
## Intro/Background
# Section 1. Statistical Test
1.1 Which statistical test did you use to analyze the NYC subway data? Did you use a one-tail or a two-tail P value? What is the null hypothesis? What is your p-critical value?
I used a two tailed Mann-Whitney U test to perform an analysis on NYC subway data. Intuitively, one would think that rain would increase subway riders but we are no evidence to make this hypothesis. Therefore, I used a two-tailed test with the null hypothesis that the two populations are the same (rain does not effect how many people use the subway) and alternative hypothesis that the populations are different (rain does effect how many people use the subway). This test was run using a 95% confidence or p-critical of 0.05.

1.2 Why is this statistical test applicable to the dataset? In particular, consider the assumptions that the test is making about the distribution of ridership in the two samples.
The histogram of the hourly entries when it was raining and not raining was non-normal (see Figure X). Therefore, Welch’s t-test is not appropriate. I decided to use a non-parametric test (Mann-Whitney U test) because it does not assume the data was drawn from any underlying probability distribution.

1.3 What results did you get from this statistical test? These should include the following numerical values: p-values, as well as the means for each of the two samples under test.
Code and output shown below