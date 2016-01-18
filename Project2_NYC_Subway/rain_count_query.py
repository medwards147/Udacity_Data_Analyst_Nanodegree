import pandas
import pandasql             
import csv
import matplotlib.pyplot as plt
import numpy as np

def num_rainy_days(filename):
    '''
    converts a CSV file into a dataframe and runs a SQL query, returning a
    count of days when it rained.
    '''
    weather_data = pandas.read_csv(filename)
    weather_data.rename(columns = lambda j: j.replace(' ', '_').lower(), 
                        inplace=True)

    q = """
    SELECT count(*)
    FROM weather_data
    WHERE rain=1;
    """

    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days
      
def max_temp_aggregate_by_fog(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return two columns and
    two rows - whether it was foggy or not (0 or 1) and the max
    maxtempi for that fog value (i.e., the maximum max temperature
    for both foggy and non-foggy days).  The dataframe will be 
    titled 'weather_data'. You'll need to provide the SQL query.

    '''
    weather_data = pandas.read_csv(filename)
    weather_data.rename(columns = lambda j: j.replace(' ', '_').lower(), 
                        inplace=True)

    q = """
    SELECT fog, max(cast(maxtempi as integer))
    FROM weather_data
    GROUP BY fog;
    """
    
    #Execute your SQL command against the pandas frame
    foggy_days = pandasql.sqldf(q.lower(), locals())
    return foggy_days

def avg_weekend_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - the average meantempi on days that are a Saturday
    or Sunday (i.e., the the average mean temperature on weekends).
    The dataframe will be titled 'weather_data' and you can access
    the date in the dataframe via the 'date' column.
    '''
    weather_data = pandas.read_csv(filename)
    weather_data.rename(columns = lambda j: j.replace(' ', '_').lower(), 
                        inplace=True)
    weather_data.rename(columns={'daten':'date'}, inplace=True) 

    q = """
    SELECT avg( cast (meantempi as integer))
    FROM weather_data
    WHERE cast (strftime('%w', date) as integer) = 0 or cast (strftime('%w', date) as integer) = 6;
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends
    
def avg_min_temperature(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data. More specifically you want to find the average
    minimum temperature (mintempi column of the weather dataframe) on 
    rainy days where the minimum temperature is greater than 55 degrees.
 
     '''
    weather_data = pandas.read_csv(filename)
    weather_data.rename(columns = lambda j: j.replace(' ', '_').lower(), 
                        inplace=True)
    
    q = """
    SELECT avg( cast (mintempi as integer))
    FROM weather_data
    WHERE rain = 1 and mintempi > 55
    """
    
    #Execute your SQL command against the pandas frame
    avg_min_temp_rainy = pandasql.sqldf(q.lower(), locals())
    return avg_min_temp_rainy
    
def fix_turnstile_data(filenames):
    '''
    Filenames is a list of MTA Subway turnstile text files. A link to an example
    MTA Subway turnstile text file can be seen at the URL below:
    http://web.mta.info/developers/data/nyct/turnstile/turnstile_110507.txt
    
    As you can see, there are numerous data points included in each row of the
    a MTA Subway turnstile text file. 

    You want to write a function that will update each row in the text
    file so there is only one entry per row. A few examples below:
    A002,R051,02-00-00,05-28-11,00:00:00,REGULAR,003178521,001100739
    A002,R051,02-00-00,05-28-11,04:00:00,REGULAR,003178541,001100746
    A002,R051,02-00-00,05-28-11,08:00:00,REGULAR,003178559,001100775
    
    Write the updates to a different text file in the format of "updated_" + filename.
    For example:
        1) if you read in a text file called "turnstile_110521.txt"
        2) you should write the updated data to "updated_turnstile_110521.txt"

    The order of the fields should be preserved. Remember to read through the 
    Instructor Notes below for more details on the task. 
    
    In addition, here is a CSV reader/writer introductory tutorial:
    http://goo.gl/HBbvyy
    
    You can see a sample of the turnstile text file that's passed into this function
    and the the corresponding updated file in the links below:
    
    Sample input file:
    https://www.dropbox.com/s/mpin5zv4hgrx244/turnstile_110528.txt
    Sample updated file:
    https://www.dropbox.com/s/074xbgio4c39b7h/solution_turnstile_110528.txt
    '''
    
    for name in filenames:
        reader = csv.reader(open(name, 'rb'))
        new_filename = "updated_"+name
        writer = csv.writer(open(new_filename, 'wb'))
        for row in reader:
            first_3 = row[0:3]
            for i in range(3, len(row), 5):
               after_first_3 = row[i:i+5]
               writer.writerow(first_3 + after_first_3)

def create_master_turnstile_file(filenames, output_file):
    '''
    Write a function that takes the files in the list filenames, which all have the 
    columns 'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn', and consolidates
    them into one file located at output_file.  There should be ONE row with the column
    headers, located at the top of the file. The input files do not have column header
    rows of their own.
    
    For example, if file_1 has:
    line 1 ...
    line 2 ...
    
    and another file, file_2 has:
    line 3 ...
    line 4 ...
    line 5 ...
    
    We need to combine file_1 and file_2 into a master_file like below:
     'C/A, UNIT, SCP, DATEn, TIMEn, DESCn, ENTRIESn, EXITSn'
    line 1 ...
    line 2 ...
    line 3 ...
    line 4 ...
    line 5 ...
    '''
    with open(output_file, 'w') as master_file:
        column_headings = 'C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n'
        master_file.write(column_headings)
        for filename in filenames:
            # your code here
            input_file = open(filename, 'r')
            for line in input_file:
                if line.strip() == column_headings:
                    pass
                else:
                    master_file.write(line)

def filter_by_regular(filename):
    '''
    This function should read the csv file located at filename into a pandas dataframe,
    and filter the dataframe to only rows where the 'DESCn' column has the value 'REGULAR'.
    
    For example, if the pandas dataframe is as follows:
    ,C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    1,A002,R051,02-00-00,05-01-11,04:00:00,DOOR,3144335,1088159
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    3,A002,R051,02-00-00,05-01-11,12:00:00,DOOR,3144424,1088231
    
    The dataframe will look like below after filtering to only rows where DESCn column
    has the value 'REGULAR':
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    '''
    
    data = pandas.read_csv(filename)
    turnstile_data = data[data['DESCn'] == 'REGULAR']
    return turnstile_data

def get_hourly_entries(df):
    '''
    changes the cumulative entry numbers to a count of entries since the last reading
    (i.e., entries since the last row in the dataframe).
    '''
    df['ENTRIESn_hourly'] = df['ENTRIESn'] - df['ENTRIESn'].shift(periods = 1)
    df = df.fillna(1)
    return df

def get_hourly_exits(df):
    '''
    changes the cumulative exit numbers to a count of exits since the last reading
    (i.e., exits since the last row in the dataframe).
    '''
    df['EXITSn_hourly'] = df['EXITSn'] - df['EXITSn'].shift(1)
    df = df.fillna(0)
    return df

def time_to_hour(time):
    '''
    given an input variable time that represents time in the format of:
    "00:00:00" (hour:minutes:seconds)
    returns the hour as an integer
    '''
    datetime = pandas.to_datetime(time)
    hour = datetime.hour
    return hour

def reformat_subway_dates(date):
    '''
    converts dates formatted in the format month-day-year to dates formatted
    as year-month-day.
    '''

    d = datetime.strptime(date, '%m-%d-%y')
    date_formatted = d.strftime('%Y-%m-%d')
    return date_formatted


if __name__ == '__main__':
    print num_rainy_days('C:/Users/MAX/Documents/Udacity/Data Analyst Nanodegree/' +
        'Project2_Subway/turnstile_data_master_with_weather.csv')
    print max_temp_aggregate_by_fog('C:/Users/MAX/Documents/Udacity/Data Analyst Nanodegree/' +
        'Project2_Subway/turnstile_data_master_with_weather.csv')
    print avg_weekend_temperature('C:/Users/MAX/Documents/Udacity/Data Analyst Nanodegree/' + 
        'Project2_Subway/turnstile_data_master_with_weather.csv')
    print avg_min_temperature('C:/Users/MAX/Documents/Udacity/Data Analyst Nanodegree/' + 
        'Project2_Subway/turnstile_data_master_with_weather.csv')
    print "Data is now updated"
    fix_turnstile_data(['turnstile_110528.txt'])
    print open('updated_turnstile_110528.txt').read()
    create_master_turnstile_file(['updated_turnstile_110528.txt'], 'master_turnstile.txt')
    print filter_by_regular('master_turnstile.txt')    