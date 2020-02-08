import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import seaborn as sns



def four_mavg_us():
    
    acct = input('Initial Capital:  ')
    ticker = input('SPY or IWM:   ')
    start = input('Start date mm/dd/yyyy:  ')
    freq = input('Daily(d), Weekly (w), Monthly(m):   ')
    p1 = input('First SMA Periods:  ')
    p2 = input('Second SMA Periods:  ')
    p3 = input('Third SMA Periods:  ')
    p4 = input('Fourth SMA Periods:  ')
    exit_choice = input('Exit to bonds or cash:   ')
    if exit_choice == 'bonds':
        bonds = input('Short Term (shy) or Long Term (ief) bonds?:  ')
            
    if exit_choice == 'cash':
        chart_title = 'S&P500 Multiple Moving Average Strategy'+'\n'+'Exit Positions into Cash'
    elif bonds == 'shy':
        chart_title = 'S&P500 Multiple Moving Average Strategy'+'\n'+'Exit Positions into 1-3yr Treasuries'
    else:
        chart_title = 'S&P500 Multiple Moving Average Strategy'+'\n'+'Exit Positions into 7-10yr Treasuries'
    
    data = web.get_data_yahoo(ticker, start, datetime.today(), interval=freq)
    st_bonds = web.get_data_yahoo('shy',start, datetime.today(), interval=freq)
    lt_bonds = web.get_data_yahoo('ief',start, datetime.today(), interval=freq)
    
    ts = pd.Series(data['Adj Close'])
    chg = ts.pct_change() + 1
    
    ts_st_bonds = pd.Series(st_bonds['Adj Close'])
    st_chg = ts_st_bonds.pct_change() + 1    
    
    ts_lt_bonds = pd.Series(lt_bonds['Adj Close'])
    lt_chg = ts_lt_bonds.pct_change() + 1    
    
    total_cash = int(acct)
    cash1 = [total_cash/4]
    cash2 = [total_cash/4]
    cash3 = [total_cash/4]
    cash4 = [total_cash/4]

    #market = (ts / data['Adj Close'].iloc[0]) * total_cash

    bh_account = [total_cash]
    
    
    #  Buy and Hold
    for i in range(1,len(ts)):
        bh_capital = bh_account[i-1] * chg[i]
        bh_account.append(bh_capital)
    

#-----------------------------------------------------------------------#    
    
    # First Moving Average
    sma1 = pd.rolling_mean(ts,int(p1))
    
    for i in range(1, len(ts)):
        if ts[i-1] > sma1[i-1]:
            new_cash1 = cash1[i-1] * chg[i]
            cash1.append(new_cash1)
        else:
            if exit_choice == 'bonds':
                if bonds == 'shy':
                    new_cash1 = cash1[i-1] * st_chg[i]
                    cash1.append(new_cash1)
                elif bonds == 'ief':
                    new_cash1 = cash1[i-1] * lt_chg[i]
                    cash1.append(new_cash1)
            else:
                cash1.append(cash1[i-1])

    eq_curve1 = pd.Series(cash1)
 
#-----------------------------------------------------------------------#
    
    # Second Moving Average
    sma2 = pd.rolling_mean(ts,int(p2))
    
    for i in range(1, len(ts)):
        if ts[i-1] > sma2[i-1]:
            new_cash2 = cash2[i-1] * chg[i]
            cash2.append(new_cash2)
        else:
            if exit_choice == 'bonds':
                if bonds == 'shy':
                    new_cash2 = cash2[i-1] * st_chg[i]
                    cash2.append(new_cash2)
                elif bonds == 'ief':
                    new_cash2 = cash2[i-1] * lt_chg[i]
                    cash2.append(new_cash2)
            else:
                cash2.append(cash2[i-1])

    eq_curve2 = pd.Series(cash2)   
    
#-----------------------------------------------------------------------#    
    
    # Third Moving Average
    sma3 = pd.rolling_mean(ts,int(p3))
    
    for i in range(1,len(ts)):
        if ts[i-1] > sma3[i-1]:
            new_cash3 = cash3[i-1] * chg[i]
            cash3.append(new_cash3)
        else:
            if exit_choice == 'bonds':
                if bonds == 'shy':
                    new_cash3 = cash3[i-1] * st_chg[i]
                    cash3.append(new_cash3)
                elif bonds == 'ief':
                    new_cash3 = cash3[i-1] * lt_chg[i]
                    cash3.append(new_cash3)
            else:
                cash3.append(cash3[i-1])

    eq_curve3 = pd.Series(cash3)   
    
#-----------------------------------------------------------------------#

    # Fourth Moving Average
    sma4 = pd.rolling_mean(ts,int(p4))
    
    for i in range(1,len(ts)):
        if ts[i-1] > sma4[i-1]:
            new_cash4 = cash4[i-1] * chg[i]
            cash4.append(new_cash4)
        else:
            if exit_choice == 'bonds':
                if bonds == 'shy':
                    new_cash4 = cash4[i-1] * st_chg[i]
                    cash4.append(new_cash4)
                elif bonds == 'ief':
                    new_cash4 = cash4[i-1] * lt_chg[i]
                    cash4.append(new_cash4)
            else:
                cash4.append(cash4[i-1])

    eq_curve4 = pd.Series(cash4)      
    
#-----------------------------------------------------------------------#    

    
    total_eq_curve = (eq_curve1 + eq_curve2 + eq_curve3 + eq_curve4)
    bh_eq_curve = pd.Series(bh_account)
    
    # Returns Calcs
    years_diff = datetime.now().year - int(start[6:10])
    
    bh_rtn = ((bh_eq_curve.iloc[-1] / bh_eq_curve.iloc[0]) - 1) * 100
    strat_rtn = ((total_eq_curve.iloc[-1] / total_eq_curve[0]) - 1) * 100
    
    bh_cagr = (((bh_eq_curve.iloc[-1] / bh_eq_curve.iloc[0]) ** (1 / years_diff)) - 1) * 100
    strat_cagr = (((total_eq_curve.iloc[-1] / total_eq_curve.iloc[0]) ** (1 / years_diff)) - 1) * 100    
    
    
       
    
    print('')    
    print(".....................................................................")
    print(".....................       RESULTS     .............................")
    print(".....................................................................")
    print('')
    print('--> Buy and Hold <--')
    print('Account Value     '+str(round(bh_eq_curve.iloc[-1],2)))
    print('Total Return %    '+str(round(bh_rtn,1)))
    print('CAGR %            '+str(round(bh_cagr,1)))
    print('')
    print('--> Strategy <--')
    print('Account Value     '+str(round(total_eq_curve.iloc[-1],2)))
    print('Total Return %    '+str(round(strat_rtn,1)))
    print('CAGR %            '+str(round(strat_cagr,1)))
    print('')       


    # Current Positions
    print('')
    print('Current Portfolio:')
    if ts.iloc[-1] > sma1.iloc[-1]:
        print('Above '+p1+' period SMA. Allocate 25% to SPY')
    elif exit_choice == 'cash':
        print('Below '+p1+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p1+' period SMA. Allocate 25% to '+str(bonds).upper())

        
    if ts.iloc[-1] > sma2.iloc[-1]:
        print('Above '+p2+' period SMA. Allocate 25% to SPY')
    elif exit_choice == 'cash':
        print('Below '+p2+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p2+' period SMA. Allocate 25% to '+str(bonds).upper())
        

    if ts.iloc[-1] > sma3.iloc[-1]:
        print('Above '+p3+' period SMA. Allocate 25% to SPY')
    elif exit_choice == 'cash':
        print('Below '+p3+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p3+' period SMA. Allocate 25% to '+str(bonds).upper())
        

    if ts.iloc[-1] > sma4.iloc[-1]:
        print('Above '+p4+' period SMA. Allocate 25% to SPY')    
    elif exit_choice == 'cash':
        print('Below '+p4+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p4+' period SMA. Allocate 25% to '+str(bonds).upper())
        
    
    
    df_bh_eq_curve = pd.DataFrame(bh_eq_curve, columns=['Buy and Hold'])
    df_total_eq_curve = pd.DataFrame(total_eq_curve, columns=['Strategy'])
    data.reset_index(inplace=True)
    merged_df = data.join(df_total_eq_curve, how='right')
    merged_df = merged_df.join(df_bh_eq_curve, how='right')
    merged_df.set_index('Date', inplace=True)    
    
    merged_df['Buy and Hold'].plot(color='0.25', style=':', legend=True, title=str(chart_title))
    merged_df['Strategy'].plot(color='g', legend=True)



#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------#



def four_mavg_uk():
    
    acct = input('Initial Capital:  ')
    indx = input('FTSE 100 (ISF.L) or FTSE 250 (MIDD.L):    ')
    start = input('Start date mm/dd/yyyy:  ')
    freq = input('Daily(d), Weekly (w), Monthly(m):   ')
    p1 = input('First SMA Periods:  ')
    p2 = input('Second SMA Periods:  ')
    p3 = input('Third SMA Periods:  ')
    p4 = input('Fourth SMA Periods:  ')
    exit_choice = input('Exit to bonds or cash:   ')
    if exit_choice == 'bonds':
        bonds = input('0-5yr Gilts (IGLS.L) or Inf-Linked (INXG.L) bonds?:  ')
            
    if exit_choice == 'cash':
        chart_title = 'UK Multiple Moving Average Strategy'+'\n'+'Exit Positions into Cash'
    elif bonds == 'igls.l':
        chart_title = 'UK Multiple Moving Average Strategy'+'\n'+'Exit Positions into Gilts'
    else:
        chart_title = 'UK Multiple Moving Average Strategy'+'\n'+'Exit Positions into Inflation Linked'
    
    data = web.get_data_yahoo(indx, start, datetime.today(), interval=freq)
    st_bonds = web.get_data_yahoo('igls.l',start, datetime.today(), interval=freq)
    lt_bonds = web.get_data_yahoo('inxg.l',start, datetime.today(), interval=freq)
    
    ts = pd.Series(data['Adj Close'])
    chg = ts.pct_change() + 1
    
    ts_st_bonds = pd.Series(st_bonds['Adj Close'])
    st_chg = ts_st_bonds.pct_change() + 1    
    
    ts_lt_bonds = pd.Series(lt_bonds['Adj Close'])
    lt_chg = ts_lt_bonds.pct_change() + 1    
    
    total_cash = int(acct)
    cash1 = [total_cash/4]
    cash2 = [total_cash/4]
    cash3 = [total_cash/4]
    cash4 = [total_cash/4]

    #market = (ts / data['Adj Close'].iloc[0]) * total_cash

    bh_account = [total_cash]
    
    
    #  Buy and Hold
    for i in range(1,len(ts)):
        bh_capital = bh_account[i-1] * chg[i]
        bh_account.append(bh_capital)
    

#-----------------------------------------------------------------------#    
    
    # First Moving Average
    sma1 = pd.rolling_mean(ts,int(p1))
    
    for i in range(1, len(ts)):
        if ts[i-1] > sma1[i-1]:
            new_cash1 = cash1[i-1] * chg[i]
            cash1.append(new_cash1)
        else:
            if exit_choice == 'bonds':
                if bonds == 'igls.l':
                    new_cash1 = cash1[i-1] * st_chg[i]
                    cash1.append(new_cash1)
                elif bonds == 'inxg.l':
                    new_cash1 = cash1[i-1] * lt_chg[i]
                    cash1.append(new_cash1)
            else:
                cash1.append(cash1[i-1])

    eq_curve1 = pd.Series(cash1)
 
#-----------------------------------------------------------------------#
    
    # Second Moving Average
    sma2 = pd.rolling_mean(ts,int(p2))
    
    for i in range(1, len(ts)):
        if ts[i-1] > sma2[i-1]:
            new_cash2 = cash2[i-1] * chg[i]
            cash2.append(new_cash2)
        else:
            if exit_choice == 'bonds':
                if bonds == 'igls.l':
                    new_cash2 = cash2[i-1] * st_chg[i]
                    cash2.append(new_cash2)
                elif bonds == 'inxg.l':
                    new_cash2 = cash2[i-1] * lt_chg[i]
                    cash2.append(new_cash2)
            else:
                cash2.append(cash2[i-1])

    eq_curve2 = pd.Series(cash2)   
    
#-----------------------------------------------------------------------#    
    
    # Third Moving Average
    sma3 = pd.rolling_mean(ts,int(p3))
    
    for i in range(1,len(ts)):
        if ts[i-1] > sma3[i-1]:
            new_cash3 = cash3[i-1] * chg[i]
            cash3.append(new_cash3)
        else:
            if exit_choice == 'bonds':
                if bonds == 'igls.l':
                    new_cash3 = cash3[i-1] * st_chg[i]
                    cash3.append(new_cash3)
                elif bonds == 'inxg.l':
                    new_cash3 = cash3[i-1] * lt_chg[i]
                    cash3.append(new_cash3)
            else:
                cash3.append(cash3[i-1])

    eq_curve3 = pd.Series(cash3)   
    
#-----------------------------------------------------------------------#

    # Fourth Moving Average
    sma4 = pd.rolling_mean(ts,int(p4))
    
    for i in range(1,len(ts)):
        if ts[i-1] > sma4[i-1]:
            new_cash4 = cash4[i-1] * chg[i]
            cash4.append(new_cash4)
        else:
            if exit_choice == 'bonds':
                if bonds == 'igls.l':
                    new_cash4 = cash4[i-1] * st_chg[i]
                    cash4.append(new_cash4)
                elif bonds == 'inxg.l':
                    new_cash4 = cash4[i-1] * lt_chg[i]
                    cash4.append(new_cash4)
            else:
                cash4.append(cash4[i-1])

    eq_curve4 = pd.Series(cash4)      
    
#-----------------------------------------------------------------------#    

    
    total_eq_curve = (eq_curve1 + eq_curve2 + eq_curve3 + eq_curve4)
    bh_eq_curve = pd.Series(bh_account)
    
    # Returns Calcs
    years_diff = datetime.now().year - int(start[6:10])
    
    bh_rtn = ((bh_eq_curve.iloc[-1] / bh_eq_curve.iloc[0]) - 1) * 100
    strat_rtn = ((total_eq_curve.iloc[-1] / total_eq_curve[0]) - 1) * 100
    
    bh_cagr = (((bh_eq_curve.iloc[-1] / bh_eq_curve.iloc[0]) ** (1 / years_diff)) - 1) * 100
    strat_cagr = (((total_eq_curve.iloc[-1] / total_eq_curve.iloc[0]) ** (1 / years_diff)) - 1) * 100    
    
    
       
    
    print('')    
    print(".....................................................................")
    print(".....................       RESULTS     .............................")
    print(".....................................................................")
    print('')
    print('--> Buy and Hold <--')
    print('Account Value     '+str(round(bh_eq_curve.iloc[-1],2)))
    print('Total Return %    '+str(round(bh_rtn,1)))
    print('CAGR %            '+str(round(bh_cagr,1)))
    print('')
    print('--> Strategy <--')
    print('Account Value     '+str(round(total_eq_curve.iloc[-1],2)))
    print('Total Return %    '+str(round(strat_rtn,1)))
    print('CAGR %            '+str(round(strat_cagr,1)))
    print('')       


    # Current Positions
    print('')
    print('Current Portfolio:')
    if ts.iloc[-1] > sma1.iloc[-1]:
        print('Above '+p1+' period SMA. Allocate 25% to '+str(indx).upper())
    elif exit_choice == 'cash':
        print('Below '+p1+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p1+' period SMA. Allocate 25% to '+str(bonds).upper())

        
    if ts.iloc[-1] > sma2.iloc[-1]:
        print('Above '+p2+' period SMA. Allocate 25% to '+str(indx).upper())
    elif exit_choice == 'cash':
        print('Below '+p2+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p2+' period SMA. Allocate 25% to '+str(bonds).upper())
        

    if ts.iloc[-1] > sma3.iloc[-1]:
        print('Above '+p3+' period SMA. Allocate 25% t '+str(indx).upper())
    elif exit_choice == 'cash':
        print('Below '+p3+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p3+' period SMA. Allocate 25% to '+str(bonds).upper())
        

    if ts.iloc[-1] > sma4.iloc[-1]:
        print('Above '+p4+' period SMA. Allocate 25% to '+str(indx).upper())    
    elif exit_choice == 'cash':
        print('Below '+p4+' period SMA. Allocate 25% to cash')
    else:
        print('Below '+p4+' period SMA. Allocate 25% to '+str(bonds).upper())
        
    
    
    df_bh_eq_curve = pd.DataFrame(bh_eq_curve, columns=['Buy and Hold'])
    df_total_eq_curve = pd.DataFrame(total_eq_curve, columns=['Strategy'])
    data.reset_index(inplace=True)
    merged_df = data.join(df_total_eq_curve, how='right')
    merged_df = merged_df.join(df_bh_eq_curve, how='right')
    merged_df.set_index('Date', inplace=True)    
    
    merged_df['Buy and Hold'].plot(color='0.25', style=':', legend=True, title=str(chart_title))
    merged_df['Strategy'].plot(color='g', legend=True)







