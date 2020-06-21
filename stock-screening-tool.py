import pandas as pd
import quandl

quandl.ApiConfig.api_key = 'hm8hEsEo4aE6iE_yTGjw'

file = 'https://s3.amazonaws.com/quandl-production-static/BSE+Descriptions/stocks.txt'
df = pd.read_csv(file, sep='|', header=0)
#df = df['CODE']
print(df.STOCK[1500][:-11])
#print(quandl.get('BSE/'+df['CODE'][400])['Close'][-1])
