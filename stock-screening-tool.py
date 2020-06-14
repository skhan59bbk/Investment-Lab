import pandas as pd

url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
df = pd.read_html(url)

tickers = [ticker for ticker in df[0]['Symbol']]


print(len(tickers))
