## prints the highest return month and percent
def mostAlgo(time, percent):
    most = 0.0
    mostIndex = 0

    for i in range(len(percent)-1): # loops through array comparing each index
        if percent[i] > most:
            most = percent[i]
            mostIndex = i # saves index to select month to be printed

    print(f'The Highest return was {most}% during the month of {time[mostIndex]}.')