from collections import Counter

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

def least_algo(time, percent):
    least = 0.0
    least_index = 0

    for i in range(len(percent)-1): # loops through array comparing each index
        if percent[i] < least:
            least = percent[i]
            least_index = i # saves index to select month to be printed

    print(f'The Highest return was {least}% during the month of {time[least_index]}.')

# Returns months that performed better than 5%
def positive_performance(month, percent):

    count = Counter()

    for i in range(len(percent)):
        if percent[i] > 5:
            count[month[i]] += 1
    print(f'Months with a return above 5%: \n {count}')

positive_performance(['Oct', 'Dec', 'Oct', 'Feb', 'March'], [6, 3, 6, 10, 10])
