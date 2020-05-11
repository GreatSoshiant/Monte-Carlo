import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
import math
import pylab as pl
from scipy.stats import lognorm

style.use('ggplot')

day_before = input("how many days you need for API?: ")  #Days for API
cAmount = float(input("What is your Collateral amount? ")) #amount for Collateral
day_number = int(input("Enter a day numbers you want: ")) #number of days you want for simulations

## Get prices from API
r=requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=' + day_before)
prices = [x[1] for x in r.json()['prices']]
returns=[]

for i in range(len(prices)-1):
    returns.append(math.log((prices[i+1]/prices[i])))

last_price=prices[-1]

first_money= cAmount / prices[-1] #first_money is the factor of collateral amount to last price of ETH

daily_vol= statistics.stdev(returns)
daily_avr= statistics.mean(returns)
daily_var= statistics.variance(returns)
daily_drift=daily_avr+(daily_var/2)


#print("This is average of ETH history prices",daily_avr)
#print("This is standar diviation of ETH history prices",daily_vol)

drift = daily_drift
#print("This is drift of the ETH prices",daily_drift)

temprory=0


numberSimulation=1000


simulation_df = pd.DataFrame()
final_prices=[]
final_price_for_onepointfive_dollar=[]
##difference=[]
blackCoinZero=[]
logReturn=[]
positives=[]
redBellowOne=[]
leverages=[]
littleDrop=[]
fulllevrage=[]

for i in range(numberSimulation):
    count=0
    daily_vol= statistics.stdev(returns)
    daily_avr= statistics.mean(returns)
    daily_var= statistics.variance(returns)

    daily_drift=daily_avr+(daily_var/2)
    drift = daily_drift

    price_series=[]

    shock = drift + daily_vol * np.random.normal()
    price=  last_price * math.exp(shock)

    price_series.append(price)

    for y in range(day_number):
        if count == day_number-1:
            break

        shock = drift + daily_vol * np.random.normal()
        price= price_series[count] * math.exp(shock)
        price_series.append(price)

        count += 1

    simulation_df[i]=price_series

    ## final_prices is the price of all simulations on the last day of estimations
    final_prices.append(price_series[len(price_series)-1])
    final_price_for_onepointfive_dollar.append(first_money * price_series[len(price_series)-1])
    ## Log of the outcomes of each simulation on day nth (100)
    logReturn.append(math.log(first_money * price_series[len(price_series)-1]))
    alpha=(first_money * price_series[len(price_series)-1])
    ##difference.append((first_money * price_series[len(price_series)-1])-1)

    ##### In this part we assume that for cAmount (collateral) investment we have outcomes and then choose the simulaion results with :
    #####   1. outcomes lower than 1USD as redBellowOne
    #####   2. outcomes lesser and equal to one as blackCoinZero (In this part black coin is equal to zero)
    #####   3. outcomes that are higher than 1USD has a value for blackcoin --> positives
    if ((first_money * price_series[len(price_series)-1]) < 1):
        redBellowOne.append((first_money * price_series[len(price_series)-1]))
    if ((first_money * price_series[len(price_series)-1]) > 1 and (first_money * price_series[len(price_series)-1]) < cAmount ):
        littleDrop.append((first_money * price_series[len(price_series)-1]))
    if ((first_money * price_series[len(price_series)-1]) <= 1):
        blackCoinZero.append((first_money * price_series[len(price_series)-1]))
    else:
        positives.append((first_money * price_series[len(price_series)-1]))
    if ((first_money * price_series[len(price_series)-1]) >= cAmount):
        temprory=(first_money * price_series[len(price_series)-1])
        leverages.append((cAmount*temprory -1)/(cAmount*temprory -temprory))
    if ((first_money * price_series[len(price_series)-1]) >= 1):
        temprory=(first_money * price_series[len(price_series)-1])
        fulllevrage.append((cAmount*temprory -1)/(cAmount*temprory -temprory))

rednumber=len(redBellowOne)
redmean=statistics.mean(redBellowOne)
redexpected= ((redmean * rednumber)+ (1000 - rednumber))/1000
blackexpected= ((1000-rednumber)*((statistics.mean(positives))-1))/1000
print("The mean of last day outcomes is:",statistics.mean(final_price_for_onepointfive_dollar))
print("The stantard deviation of the last day outcomes is:",statistics.stdev(final_price_for_onepointfive_dollar))

print("Number of cases that Blackcoin is zero:",len(blackCoinZero))

print("Number of cases that Redcoin is bellow one dollar is:",len(redBellowOne))
print("The mean of Redcoins bellow one dollar is:",statistics.mean(redBellowOne))
print("The STdev of Redcoins bellow one dollar is:",statistics.stdev(redBellowOne))

print("Expected Value of Redcoins is:",redexpected)
print("Expected Value of Blackcoins is:",blackexpected)


print("The mean of Leverage of Blackcoin is:",statistics.mean(leverages))
print("The stantard deviation of Leverage is:",statistics.stdev(leverages))

print("The mean of fulllevrage Leverage of Blackcoin for non-zero Blackcoin cases is:",statistics.mean(fulllevrage))
print("The stantard deviation of fulllevrage of Blackcoin for non-zero Blackcoin cases is:",statistics.stdev(fulllevrage))

print("Number of cases for a little drop in ETH is:",len(littleDrop))
print("The mean of cases for a little drop in ETH is:",statistics.mean(littleDrop))
print("The stantard deviation of cases for a little drop in ETH is:",statistics.stdev(littleDrop))

standar_div = statistics.stdev(final_price_for_onepointfive_dollar)
miangin = statistics.mean(final_price_for_onepointfive_dollar)
new_drift=  miangin + (standar_div**2)/2  -cAmount

disti=lognorm([standar_div],loc=new_drift)

man=np.linspace(0,6,100)

fig20= plt.figure()
plt.hist(logReturn, density=False, bins=50)



fig0= plt.figure()
plt.hist(final_price_for_onepointfive_dollar, density=False, bins=50)
pl.plot(man,disti.pdf(man)*100)

fig= plt.figure()
plt.plot(simulation_df)


##fig2= plt.figure()
##plt.plot(final_price_for_onepointfive_dollar)


##fig3= plt.figure()
##plt.plot(difference)


fig10= plt.figure()
plt.hist(leverages, density=False, bins=100)
plt.show()


##fig4= plt.figure()
##plt.plot(blackCoinZero)

##plt.show()
