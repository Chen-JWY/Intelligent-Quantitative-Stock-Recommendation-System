import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn

cash = 100000
buypoint = []
sellpoint = []
slen = 10  #SMA
llen = 30  #LMA
Securities = {} # 'token':shares
stocks = ['IBM','AAPL']
porp = [0.5,0.5]

def init(token):
    Securities[token] = 0.0
    data = yf.Ticker(token)
    bar = data.history(interval='1d', start='2021-1-1')
    bar.to_csv('./'+str(token)+'.csv')
    bar = pd.read_csv('./'+str(token)+'.csv')
    bar['Date'] = pd.to_datetime(bar['Date'])
    plt.plot(bar['Date'],bar['Close'])
    return bar

def buy(token,share,time,price):
    global cash
    buypoint.append([time,price])
    Securities[token] = share
    cash -= share * price

def sell(token,share,time,price):
    global cash
    sellpoint.append([time,price])
    Securities[token] = 0.0
    cash += share * price
    print(cash)

def liquidate(token,price):
    global cash
    cash += Securities[token] * price
    Securities[token] = 0

def strategy(id,bar):#MACD
    tmp=pd.DataFrame({})
    token = stocks[id]
    for i in range(llen+1,len(bar)):
        tmp.loc[i,['Date']] = bar.loc[i,['Date']]
        sma_pre = bar.Close[i-slen:i].mean()
        sma_now = bar.Close[i-slen+1:i+1].mean()
        lma_pre = bar.Close[i-llen:i].mean()
        lma_now = bar.Close[i-llen+1:i+1].mean()
        tmp.loc[i,['SMA']] = sma_now
        tmp.loc[i,['LMA']] = lma_now
        if Securities[token] == 0:
            if sma_pre < lma_pre and sma_now > lma_now:
                buy(token,cash/porp[id]/bar.Close[i],bar.Date[i],bar.Close[i])
        else:
            if sma_pre > lma_pre and sma_now < lma_now:
                sell(token,Securities[token],bar.Date[i],bar.Close[i])
        plt.plot(tmp['Date'],tmp['SMA'])
        plt.plot(tmp['Date'],tmp['LMA'])

def plot():
    plt.xlabel('Date')
    plt.ylabel('Price(USD)')
    plt.legend(['Close', 'MA' + str(slen), 'MA' + str(llen)], loc='upper left')
    plt.show()


if __name__ == '__main__':
    main()
