from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt

def dataFrame():
    pd.set_option("display.max_rows", 202, "display.max_columns", None) #shows all columns in the dataframes

    df = pd.DataFrame(inflation_crawler(), columns=['years', 'InflationRate%']) #creates data frame
    df2 = pd.DataFrame(spx_crawler(), columns=['years', 'SPXROI%'])

    result = pd.merge(df, df2, on='years') #merges the dataframes
    print(result)

    result.plot(x='years', y=['InflationRate%', 'SPXROI%'], kind='line') #plots the data
    plt.show()


def inflation_crawler():
    source = "https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-" #source of data
    code = requests.get(source) #gets html
    content = code.content #gets content of html
    soup = BeautifulSoup(content, features="lxml") #cleans html a little bit and sets it up to be parsed
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
    url = 'https://www.macrotrends.net/2526/sp-500-historical-annual-returns'
    html = requests.get(url)
    text = html.text
    soup = BeautifulSoup(text, 'html.parser')
    allData = []
    for datas in soup.findAll('td'):
        data = datas.string
        allData.append(data)

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

    spxdata = {"years": years,"SPXROI%": ROI}

    return spxdata

#cisco BTC crawler
def btc_crawler():
    url = "https://www.in2013dollars.com/bitcoin-price"

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="html.parser")

    btc_yearly_table = soup.find('table', {"class": "table table-striped"})
    print(btc_yearly_table.text)

dataFrame()