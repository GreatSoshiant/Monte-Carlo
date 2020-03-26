import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import statistics
import math

style.use('ggplot')

r=requests.get('https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=1000')
prices = [x[1] for x in r.json()['prices']]
returns=[]
for i in range(len(prices)-1):
    returns.append((prices[i+1]-prices[i])/prices[i])

last_price=prices[-1]
first_money= 1.5 / prices[-1]

numberSimulation=1000

day_number=x = int(input("Enter a day numbers you want: "))
simulation_df = pd.DataFrame()
final_prices=[]
final_price_for_onepointfive_dollar=[]
difference=[]
for i in range(numberSimulation):
    count=0
    daily_vol= statistics.stdev(returns)
    daily_avr= statistics.mean(returns)
    daily_var= statistics.variance(returns)

    daily_drift=daily_avr-(daily_var/2)
    drift = daily_drift - 0.5 * daily_vol ** 2

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
    final_prices.append(price_series[len(price_series)-1])
    final_price_for_onepointfive_dollar.append(first_money * price_series[len(price_series)-1])
    difference.append((first_money * price_series[len(price_series)-1])-0.5)
print(statistics.mean(final_prices),statistics.stdev(final_prices))

fig= plt.figure()
plt.plot(simulation_df)



fig2= plt.figure()
plt.plot(final_price_for_onepointfive_dollar)


fig3= plt.figure()
plt.plot(difference)
plt.show()
