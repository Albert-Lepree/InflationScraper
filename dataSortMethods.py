## prints the highest return month and percent
def mostAlgo(time, percent):
    most = 0.0
    mostIndex = 0

    for i in range(len(percent)-1): # loops through array comparing each index
        if percent[i] > most:
            most = percent[i]
            mostIndex = i # saves index to select month to be printed

    print(f'The Highest return was {most}% during the month of {time[mostIndex]}.')

    # counts how many times btc was up and spx was dont => btc was down and spx was up
def similarityAlgo(btc, spx):

    BTCupSPXdown = 0
    BTCdownSPXup = 0
    BTCupSPXup = 0
    BTCdownSPXdown = 0

    for i in range(len(btc) - 1):
        if btc[i]> 0 and spx[i] <0:
            BTCupSPXdown+=1
        elif btc[i]<0 and spx[i]> 0:
            BTCdownSPXup+=1
        elif btc[i] < 0 and spx[i] < 0:
            BTCdownSPXdown+=1
        elif btc[i] > 0 and spx[i] > 0:
            BTCupSPXup+=1

    print(f'Bitcoin was positive while the S&P was negative {BTCupSPXdown} times since inception')
    print(f'Bitcoin was negative while the S&P was positive {BTCdownSPXup} times since inception')
    print(f'Bitcoin was positive while the S&P was positive {BTCupSPXup} times since inception')
    print(f'Bitcoin was negative while the S&P was negative {BTCdownSPXdown} times since inception')
