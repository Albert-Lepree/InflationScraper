from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

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

    ## End Data cleaning

    month = []
    percent = []

    for i in range(len(array)): # separates the data into 2 arrays by even or odd index
        if i%2 == 1:
            month.append(array[i])
        else:
            array[i] = array[i].rstrip((array[i])[-1])  # removes % sign to be converted to float
            percent.append(float(array[i]))  # adds ROI to list and converts to float

    data = {'month' : month, "%return" : percent} # puts data into an array? to be put into data frame
    df = pd.DataFrame(data, columns=['month', '%return']) #creates dataframe
    print(df)
    df.plot(x='month', y='%return', kind='line') #plots the data
    plt.show()

monthly_btc_crawler()