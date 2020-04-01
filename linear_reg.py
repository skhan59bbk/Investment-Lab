import random as rand
import matplotlib.pyplot as plt
import numpy as np
import quandl
import pandas as pd

plt.style.use('ggplot')
rand.seed(11)


def create_dataset(n, variance, step=2, corr=False):

    val = 1
    y = []
    for i in range(n):
        num = val + rand.randrange(-variance, variance)
        y.append(num)
        if corr and corr == 'pos':
            val += step
        elif corr and corr == 'neg':
            val -= step
    x = [i for i in range(len(y))]
    
    return np.array(x), np.array(y)


def data_from_quandl(ticker):

    key = "ADD KEY HERE"
    data = quandl.get(ticker, api_key=key)
    returns = data['Last'].pct_change(periods=1)[-1000:]

    return returns


def average(nums):
    
    count = 0
    total = 0
    for i in nums:
        count += 1
        total += i
    return total / count


def x_y_bars():

    x_bar = average(x)
    y_bar = average(y)
    xy_bar = average(x*y)
    x2_bar = average(x**2)

    return x_bar, y_bar, xy_bar, x2_bar
    

def best_fit_line():

    x_bar, y_bar, xy_bar, x2_bar = x_y_bars()

    m = sum((x-x_bar)*(y-y_bar)) / sum((x-x_bar)**2)
    b = y_bar - (m * x_bar)
    
    return m, b


def r_squared():

    x_bar, y_bar, xy_bar, x2_bar = x_y_bars()
    m, b = best_fit_line()

    ss_res = sum((y - ((m*x)+b))**2)
    ss_tot = sum((y - y_bar)**2)

    r_sq = round(1 - (ss_res/ss_tot), 3)

    return r_sq
    

x, y = create_dataset(100, 50, 2, 'neg')
##x = data_from_quandl('CHRIS/CME_ES1')
##y = data_from_quandl('CHRIS/CME_Z1')

m, b = best_fit_line()
reg_line = [((m*X)+b) for X in x]

##new_x = np.array([2.5, 5.5, 8.5])
##predict_y = (m * new_x) + b

print(round(m,3), round(b,3))
print(r_squared())


plt.scatter(x, y, color='blue')
plt.plot(x, reg_line, color='red')
plt.legend(['R squared: '+str(r_squared())])
plt.show()


