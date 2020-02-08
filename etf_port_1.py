import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
sns.set(style="darkgrid")


def read_data():
    try:
        f = pd.read_csv('C:\\Users\\samee\\Documents\\Datasets\\etf_prices.csv')
        f = f.set_index('Date')
        return f
    
    except Exception as e:
        print(str(e))


def print_tickers():
    df = read_data()
    for col in df.columns:
        print(col)


def last_price(ticker=None):
    df = read_data()
    if ticker == None:
        price = df[-1:]
    else:
        price = df[ticker][-1:]
    return price


def date_range():
    df = read_data()
    first, last = df.index.values[1], df.index.values[-1]
    return first +' to '+ last


def hist_price(ticker=None, date=None):
    df = read_data()
    try:
        if ticker == None:
            price = df.loc[date]
            return date, ticker, price
        else:
            price = df[ticker].loc[date]
            return date, ticker, price
    except Exception:
        valid_range = date_range()
        print('Available date range: '+str(valid_range))


def first_valid_date():
    df = read_data()
    start_dates = []
    for ticker in df.columns:
        start = df[ticker].first_valid_index()
        start_datetime = dt.datetime.strptime(start, '%d/%m/%Y')
        start_dates.append(start_datetime.date())
    earliest_start = max(start_dates)
    base = earliest_start.strftime('%d/%m/%Y')
    return base


def norm_prices():
    df = read_data()
    base = first_valid_date()
    df_adj = df[base:]
    df_norm = ((df_adj / df.loc[base])-1) *100
    return df_norm


def returns(start_dt=None, end_dt=None):
    df = read_data()
    base = first_valid_date()
    if start_dt == None:
        df_adj = df[base:end_dt]
        rets = df_adj.pct_change(periods=1)
        return rets
    else:
        df_adj = df[start_dt:end_dt]
        rets = df_adj.pct_change(periods=1)
        return rets


def cum_returns(start_dt=None, end_dt=None):
    rets = returns(start_dt, end_dt)
    cum_rets = rets.cumsum()
    #for ticker in cum_rets.columns:
    #    print(cum_rets[ticker][-1:])
    return cum_rets


def plot_viz():
    #norm = norm_prices()
    #norm['SEML'].plot(figsize=(10,7), title='ETF Returns', legend=True)
    
    cum_sum = cum_returns('01/01/2018','05/05/2019')
    cum_sum.plot(figsize=(10,7), title='ETF Cumulative Returns')
    

def main():
    #print_tickers()
    #print(last_price())
    #print(hist_price('HYLD','02/11/2018'))
    plot_viz()
    #print(norm_prices())
    #print(returns())
    #print(date_range())
    #print(first_valid_date())
   


'''    
allocations = [353,184,157,85,84,45,41,41,34]
position_values = allocations * port
position_values['PORTFOLIO'] = position_values.sum(axis=1)

print(position_values['PORTFOLIO'].tail(15))
position_values['PORTFOLIO'].plot(figsize=(8,5))
'''



if __name__ == "__main__":
    main()
