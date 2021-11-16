from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

#################################################################
# Gets the data from each crawler and CSV extractor method and
# puts it into a dataframe, then plots it in various ways
#################################################################
def merge_and_plot_data():
    pd.set_option("display.max_rows", 202, "display.max_columns", None) # shows all columns in the dataframes

    df = pd.DataFrame(monthly_btc_crawler(), columns=['month', 'BTCMonthlyChange']) # creates data frame
    df2 = pd.DataFrame(percent_change_CSV(), columns=['month', 'DXYMonthlyChange', 'SPXMonthlyChange'])

    result = pd.merge(df, df2, on='month') # merges the dataframes

    print(result)

    result.plot(x='month', y=['BTCMonthlyChange', 'DXYMonthlyChange', 'SPXMonthlyChange'], kind='line') # plots the data as a line graph
    plt.show()



    BTCChange = result.BTCMonthlyChange # assigns each column to a variable
    DXYChange = result.DXYMonthlyChange
    SPXChange = result.SPXMonthlyChange

    # violin plots
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3)

    # Plot violin plot on axes 1
    ax1.violinplot(BTCChange, showmedians=True)
    ax1.set_title('BTC%Change')

    # Plot violin plot on axes 2
    ax2.violinplot(DXYChange, showmedians=True)
    ax2.set_title('DXY%Change')

    # Plot violin plot axes 3
    ax3.violinplot(SPXChange, showmedians=True)
    ax3.set_title('SPX%Change')

    plt.show()

#################################################################
# Converts months such as 'october 2017' to 10/17
#################################################################
def month_convertor(months):

    formattedMonths = []

    for i in range(len(months)):
        year = months[i][-2] + months[i][-1]
        size = len(months[i])
        theMonth = months[i][:size - 5]
        formatted = ''
        #print(theMonth)
        if theMonth == 'January':
            formatted = '1'
        elif theMonth == 'February':
            formatted = '2'
        elif theMonth == 'March':
            formatted = '3'
        elif theMonth == 'April':
            formatted = '4'
        elif theMonth == 'May':
            formatted = '5'
        elif theMonth == 'June':
            formatted = '6'
        elif theMonth == 'July':
            formatted = '7'
        elif theMonth == 'August':
            formatted = '8'
        elif theMonth == 'September':
            formatted = '9'
        elif theMonth == 'October':
            formatted = '10'
        elif theMonth == 'November':
            formatted = '11'
        elif theMonth == 'December':
            formatted = '12'
        formatted = formatted + '/' + year
        formattedMonths.append(formatted)

    #print(formattedMonths)

    return formattedMonths


#################################################################
# Gets monthly percent change in Bitcoin since 2016 and
# transforms it to be put in the data frame
#################################################################
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

    data = {'month' : month_convertor(month), "BTCMonthlyChange" : percent} # puts data into an array? to be put into data frame


    return data

#################################################################
# Extracts Data from the 'percentChangeDXY.csv' and 'SP500.csv' then transforms it
# to be put in the data frame
#################################################################
def percent_change_CSV():

    DXY_df = pd.read_csv('./percentChangeDXY.csv')
    SPX_df = pd.read_csv('./SP500.csv')

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

    data = {'month': month_convertor(DXY_df['month']), "DXYMonthlyChange": DXY_df['DXY%return'], "SPXMonthlyChange": SPX_df['SP500_PCH']}

    return data

merge_and_plot_data()