from collections import Counter

## prints the highest return month and percent
def most_algo(time, percent):
    most = 0.0
    most_index = 0

    for i in range(len(percent)-1): # loops through array comparing each index
        if percent[i] > most:
            most = percent[i]
            most_index = i # saves index to select month to be printed

    print(f'The Highest return was {most}% during the month of {time[most_index]}.')

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


