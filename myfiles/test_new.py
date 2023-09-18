# find the compound intrest 

def compound_intrest(principle, rate, time):
    amount = principle * (pow((1 + rate / 100), time))
    ci = amount - principle
    return ci

principle = int(input("Enter the principle: "))
rate = int(input("Enter the Rate: "))
time = int(input('Enter the Time in years: '))

print(f'The Compound Intrest of Rs {principle} at the rate of {rate} in {time} years is {compound_intrest(principle, rate, time)}.')
