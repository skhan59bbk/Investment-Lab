import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

directory = 'C://Users//samee//Documents//Datasets//'

oil = pd.read_csv(directory+'pwd-oil-prices.csv')
gas = pd.read_csv(directory+'pwd-gas-prices.csv')
gold = pd.read_csv(directory+'pwd-gold-prices.csv')

#df = pd.DataFrame(data=[oil, gas, gold], columns = ['Date', 'Oil', 'Gas', 'Gold'])

oil.columns = ['Date', 'Price']
gas.columns = ['Date', 'Price']
gold.columns = ['Date', 'Price']

#gold['Date'] = pd.to_datetime(gold['Date'])

oil = oil.set_index('Date')
gas = gas.set_index('Date')
gold = gold[175:].set_index('Date')

oil['Pct_Chg'] = oil['Price'].pct_change()


print(oil.Pct_Chg.describe())

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'hspace':0, 'height_ratios':[3,1]})
fig.autofmt_xdate()
ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
ax2.xaxis.set_major_locator(plt.MaxNLocator(10))

ax1.plot(oil.Price)
ax2.plot(oil.Pct_Chg, color='r')

plt.show()
