from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

def merge_and_plot_data():
    pd.set_option("display.max_rows", 202, "display.max_columns", None) #shows all columns in the dataframes

    df = pd.DataFrame(monthly_btc_crawler(), columns=['month', 'BTCROI%']) #creates data frame
    df2 = pd.DataFrame(percent_change_DXY(), columns=['month', 'DXY%return'])

    result = pd.merge(df, df2, on='month') #merges the dataframes
    #print(result)

    result.plot(x='month', y=['BTCROI%', 'DXY%return'], kind='line') #plots the data
    #plt.show()

def monthly_btc_crawler():
    pd.set_option("display.max_rows", 202, "display.max_columns", None)  # shows all columns in the dataframes

    url = "https://www.statmuse.com/money/ask/bitcoin+return+month+by+month+2015-2021"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")

    ## begin Data cleaning: puts the data in a form that can be manipulated easier (ETL)
    soup = str(soup)
    soup = soup.replace(":", '')
    soup = soup.replace("display", '')
    soup = soup.replace("ASSET", '')
    soup = soup.replace("MONTH", '')
    soup = soup.replace("Bitcoin (BTC)", '')
    soup = soup.replace(',', '')
    soup = soup.replace('value', '')
    soup = soup.replace('{', '')
    soup = soup.replace('}', '')
    soup = soup.replace('"', '\n')
    soup = soup.replace('% RETURN', '')
    soup = soup.replace('label', '')
    soup = soup.replace('color', '')
    soup = soup.replace('[', '')
    soup = soup.replace(']', '')
    array = soup.split('\n')

    for i in range(len(array) - 1, 0, -1):
        if array[i] == '':
            array.pop(i)

    for i in range(1033, 0, -1):
        array.pop(i)


    for i in range(len(array)-1, 327, -1):
        array.pop(i)

    array.pop(0)

    for i in range(len(array) - 2, 0, -2): # deletes un needed data
        array.pop(i)

    array.pop(0) #pop bottom 4 indexes because they are un needed
    array.pop(0)
    array.pop(0)
    array.pop(0)

    month = []
    percent = []

    for i in range(len(array)): # separates the data into 2 arrays by even or odd index
        if i%2 == 1:
            month.append(array[i])
        else:
            array[i] = array[i].rstrip((array[i])[-1])  # removes % sign to be converted to float
            percent.append(float(array[i]))  # adds ROI to list and converts to float

    ## End Data cleaning

    data = {'month' : month, "BTCROI%" : percent} # puts data into an array? to be put into data frame
    df = pd.DataFrame(data, columns=['month', 'BTCROI%']) #creates dataframe


    return data


def percent_change_DXY():

    DXY_df = pd.read_csv('./percentChangeDXY.csv')

    # Convert the date data to datetime
    dates = pd.Series(DXY_df['DATE'])
    dates = pd.to_datetime(dates)

    # Getting month name from month
    # Need to rename this variable
    DXY_df['MONTH'] = dates.dt.month_name(locale = 'English')

    # Getting Year
    DXY_df['Year'] = DXY_df['DATE'].str[0:4]

    # New column with month and year
    DXY_df['month'] = DXY_df['MONTH'] + " " + DXY_df['Year']

    # Plot Date vs % Return
#    print(DXY_df.columns)
#    DXY_df.plot(x='month', y='DXY%return', kind='line')
#    plt.xticks(rotation=90)
#    plt.show()

    data = {'month': DXY_df['month'], "DXY%return": DXY_df['DXY%return']}

    return data

merge_and_plot_data()