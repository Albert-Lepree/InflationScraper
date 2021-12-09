from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import time
import dataSortMethods

def dataFrame():
    pd.set_option("display.max_rows", 202, "display.max_columns", None) #shows all columns in the dataframes

    BTCROI = btc_crawler()
    SPXROI = spx_crawler()

    df = pd.DataFrame(inflation_crawler(), columns=['years', 'InflationRate%']) #creates data frame
    df2 = pd.DataFrame(SPXROI, columns=['years', 'SPXROI'])
    df3 = pd.DataFrame(BTCROI, columns=['years', 'BTCROI'])


    result = pd.merge(df, df2, on='years') #merges the dataframes
    result = pd.merge(result, df3, on='years')
    print(result)
    print()

    print('annual')
    dataSortMethods.similarityAlgo(BTCROI['BTCROI'], SPXROI['SPXROI']) # compares returns of SPX and BTC by positivity
    print()
    print('SPX: ')
    dataSortMethods.best_inflation_investment(result['InflationRate%'], result.SPXROI, 2)
    print('BTC: ')
    dataSortMethods.best_inflation_investment(result['InflationRate%'], result.BTCROI, 2)

    result.plot(x='years', y=['InflationRate%', 'SPXROI', 'BTCROI'], kind='line') #plots the data
    plt.show()
    result.plot(x='years', y=['InflationRate%', 'SPXROI'], kind='line')
    plt.show()


def inflation_crawler():
    source = "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-" #source of data
    code = requests.get(source) #gets html
    content = code.content #gets content of html
    soup = BeautifulSoup(content, 'html.parser') #cleans html a little bit and sets it up to be parsed
    dataList = [] #empty list to be filled
    for datas in soup.findAll(style="text-align: center;"): #parses through data adding each value to the list
        dataList.append(datas.string)

    num = len(dataList) - 2 #gets top index to be deleted

    for i in range(num, 0, -3): #deletes un-needed data
        dataList.pop(i)

    dataList.pop(len(dataList) - 1)
    dataList.pop(len(dataList) - 1) #removes 2021 data because its inaccurate
    num = len(dataList) -1 #gets top index
    years = []
    annualInflation = []

    for j in range(2, num, 2): #formats data for readability and technically deletes year 1913 (because inflation data missing)
        dataList[j+1] = dataList[j+1].rstrip((dataList[j+1])[-1]) #remove percentage sign

        if len(dataList[j]) > 4: #removes spaces
            dataList[j] = dataList[j][1:]

        years.append(int(dataList[j])) #add years to list of years
        annualInflation.append(float(dataList[j+1])) #add inflation to list of inflation data and convert to a float

    inflationData = {'years': years, 'InflationRate%': annualInflation}  # puts the data into an array for the dataframe

    return inflationData

def spx_crawler():
    # EXTRACT
    url = 'https://www.macrotrends.net/2526/sp-500-historical-annual-returns'
    html = requests.get(url)

    # TRANSFORM
    text = html.text
    soup = BeautifulSoup(text, 'html.parser')
    allData = []
    for datas in soup.findAll('td'): # finds all strings with 'td' tag
        data = datas.string          # converts from html to string
        allData.append(data)         # adds data to array

    years = []
    ROI = []

    num = len(allData) -1
    for j in range(0, 12): #removes unneeded strings scraped from web
        allData.pop(num - j)

    num = len(allData) -1
    for i in range(num, 0, -7):
        allData[i] = allData[i].rstrip((allData[i])[-1]) #removes % sign to be converted to float
        ROI.append(float(allData[i])) #adds ROI to list and converts to float
        years.append(int(allData[i-6])) #adds years to list and converts to int

    spxdata = {"years": years,"SPXROI": ROI}

    return spxdata

#cisco BTC crawler
def btc_crawler():
    pd.set_option("display.max_rows", 202, "display.max_columns", None)  # shows all columns in the dataframes

    url = "https://www.in2013dollars.com/bitcoin-price"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")

    btc_yearly_table = soup.find_all('table', {"class": "table table-striped"})
    time.sleep(5)

    Years = []
    annual_change = []

    for row in btc_yearly_table:

        # Using enumerate so I can use the line count to find 'td'
        #   tags that contain year or Annual BTC % change.
        for count, td in enumerate(row.find_all('td')):

            # Grabs Rows with Year Data or Grabs Rows w/ % Change
            if (count % 4) == 0 or ((count + 1) % 4) == 0:

                # Insert into Year Column in Dataframe
                if len(td.text) == 4:
                    Years.append(int(td.text))

                # Insert into Annual % Column in Dataframe
                else:
                    tdtext = td.text.replace(',', '')
                    annual_change.append(float(tdtext))

        break  # Want the for loop to run only once

    for i in range(2009, 1927, -1): #adds non existing years so it can be merged easier
        Years.append(i)
        annual_change.append(0)

        num = len(Years) - 1

    for j in range(0, num): #reverses data to be put into dataframe

        if j > (num - j):
            break

        temp1 = Years[j]
        temp2 = annual_change[j]
        Years[j] = Years[num - j]
        Years[num - j] = temp1
        annual_change[j] = annual_change[num - j]
        annual_change[num - j] = temp2

    data = {'years': Years, 'BTCROI': annual_change}
    return data

