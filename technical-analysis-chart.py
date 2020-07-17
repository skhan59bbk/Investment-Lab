import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file = 'C://Users//samee//Documents//Datasets//EOD-AAPL.csv'

df = pd.read_csv(file)
df = df[['Date', 'Adj_Open', 'Adj_High', 'Adj_Low', 'Adj_Close', 'Adj_Volume']]
df = df.rename(columns={'Adj_Open':'Open', 'Adj_High':'High', 'Adj_Low':'Low', 'Adj_Close':'Close', 'Adj_Volume':'Volume'})
#df = df.set_index('Date')

#print(df.head())


def sma(series, periods):

    df['sma_'+str(periods)] = df[series].rolling(window=periods).mean()

    return df['sma_'+str(periods)]


def ema(series, periods):

    df.reset_index(inplace=True)
    
    multiplier = 2 / (periods + 1)

    conditions = [(df.index < periods), (df.index >= periods)]
    values = [sma('Close', periods), 1]

    df['ema_'+str(periods)] = np.select(conditions, values)

    for i in range(periods, len(df)):
        df['ema_'+str(periods)].loc[i] = (df['Close'].loc[i] * multiplier) + (df['ema_'+str(periods)].loc[i-1] * (1 - multiplier))
    
    return df['ema_'+str(periods)]
    
    
def rsi(periods):

    df['Change'] = df['Close'].diff()

    df['up'] = np.select([(df['Change'] > 0), (df['Change'] < 0)], [(df['Change']), (0)])
    df['dn'] = np.select([(df['Change'] < 0), (df['Change'] > 0)], [(df['Change']), (0)])
    
    df['avg_up'] = df['up'].rolling(window=periods+1).mean() 
    df['avg_dn'] = df['dn'].rolling(window=periods+1).mean() 

    for i in range(periods+1, len(df)):
        df['avg_up'].loc[i] = ((df['avg_up'].loc[i-1] * (periods-1)) + df['up'].loc[i]) / periods
        df['avg_dn'].loc[i] = ((df['avg_dn'].loc[i-1] * (periods-1)) + df['dn'].loc[i]) / periods
    
    df['RS'] = df['avg_up'] / abs(df['avg_dn'])
    df['RSI'] = np.select([(df['avg_dn'] == 0), (df['avg_up'] == 0), (df['RS'].notna())], [(100), (0), (100 - (100 / (1+df['RS'])))])

    return df['RSI']


def macd(fast, slow, signal):

    df['macd'] = sma('Close', fast) - sma('Close', slow)
    df['macd_signal'] = df['macd'].rolling(window=signal).mean()

    return df[['macd', 'macd_signal']]



##fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
##df['Close'].plot(ax=ax[0,0])
###sma(50).plot()
##macd(12, 26, 9).plot(ax=ax[0,1])
##plt.show()

#print(df.tail(20))

#df = df.set_index('Date')
##df.Close.plot()
##ema('Close', 50).plot()
##sma('Close', 50).plot()
##plt.show()

