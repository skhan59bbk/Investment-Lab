import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

directory = 'C://Users//samee//Documents//Datasets//'

# read data
oil = pd.read_csv(directory+'pwd-oil-prices.csv')
gas = pd.read_csv(directory+'pwd-gas-prices.csv')
gold = pd.read_csv(directory+'pwd-gold-prices.csv')

# set column names
oil.columns = ['Date', 'Price']
gas.columns = ['Date', 'Price']
gold.columns = ['Date', 'Price']

# set Date as index
oil = oil.set_index('Date')
gas = gas.set_index('Date')
gold = gold[175:].set_index('Date')

# add percent change column
oil['Pct_Chg'] = oil['Price'].pct_change()
gas['Pct_Chg'] = gas['Price'].pct_change()
gold['Pct_Chg'] = gold['Price'].pct_change()

# assign dataframe names
oil.name, gas.name, gold.name = 'oil', 'gas', 'gold'


def viz(asset):
    print(asset.Pct_Chg.describe())

    fig, (ax0, ax1, ax2) = plt.subplots(3, 1, sharex=True, gridspec_kw={'hspace':0, 'height_ratios':[3,2,1]})
    fig.autofmt_xdate()
    ax0.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax1.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax2.xaxis.set_major_locator(plt.MaxNLocator(10))

    ax0.plot(asset.Price)
    ax1.plot(np.cumsum(asset.Pct_Chg), color='g')
    ax2.plot(asset.Pct_Chg, color='r')

    ax0.title.set_text(str(asset.name))
    plt.show()


viz(gas)
