import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
from numpy import ndarray
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame


class Result:
    startCash = 0
    Cash = 0
    Share = 0
    Return = 0
    Alpha = 0
    Beta = 0
    buypoint = []
    sellpoint = []

    def __init__(self):
        pass

    def cal(self, bar, BMbar):
        self.Cash += bar.iloc(-1,4) * self.Share
        self.Return = (self.Cash - self.startCash)/self.startCash

    def show(self, bar, BMbar):
        #self.cal(bar, BMbar)
        print("startCash:",str(self.startCash))
        print("Cash:",str(self.Cash))
        print("Share:",str(self.Share))
        print("buy:",self.buypoint)
        print("sell:",self.sellpoint)

    def setcash(self, Cash):
        self.startCash = self.Cash = Cash


class Strategy(Result):
    def __init__(self):
        pass

    def sell(self, time, price, shares):
        #limit
        self.Cash += price * shares
        self.Share -= shares
        sellpoint.append([time,price])

    def buy(self, time, price, shares):
        #limit
        print(shares)
        print(price)
        self.Cash -= price * shares
        self.Share += shares
        self.buypoint.append([time,price])

    def liquidate(self, time, price):
        self.Cash -= self.Share * price
        self.Share = 0
        self.sellpoint.append([time,price])

    def train(self, starttime, endtime):
        pass

    def test(self, starttime, endtime):
        pass


class _MACD(Strategy):
    slen = 0
    llen = 0
    def __init__(self,slen=20,llen=60):
        self.slen = slen
        self.llen = llen

    def train(self, starttime, endtime):
        pass

    def test(self, bar, starttime, endtime):
        tmp = pd.DataFrame({})
        llen = self.llen
        slen = self.slen
        for i in range(llen + 1, len(bar)):
            tmp.loc[i, ['Date']] = bar.loc[i, ['Date']]
            sma_pre = bar.Close[i - slen:i].mean()
            sma_now = bar.Close[i - slen + 1:i + 1].mean()
            lma_pre = bar.Close[i - llen:i].mean()
            lma_now = bar.Close[i - llen + 1:i + 1].mean()
            # tmp.loc[i, ['SMA']] = sma_now
            # tmp.loc[i, ['LMA']] = lma_now
            if self.Share == 0:
                if sma_pre < lma_pre and sma_now > lma_now:
                    self.buy(bar.Date[i], bar.Close[i], self.Cash / bar.Close[i])
            else:
                if sma_pre > lma_pre and sma_now < lma_now:
                    self.liquidate(bar.Date[i],bar.Close[i])
            # plt.plot(tmp['Date'], tmp['SMA'])
            # plt.plot(tmp['Date'], tmp['LMA'])


class StrLib():
    MACD = _MACD()

    def __init__(self):
        pass


class Stock(StrLib):
    token = ''
    data = None
    bar = None

    def __init__(self, token, timedelta, starttime):
        self.token = token
        self.data = yf.Ticker(token)
        self.bar = self.data.history(interval=timedelta, start=starttime)
        self.bar.to_csv('./' + str(self.token) + '.csv')
        self.bar = pd.read_csv('./' + str(self.token) + '.csv')


class StockLib:
    Stocks = []
    BM = None

    def __init__(self):
        pass

    def addstock(self, Stock):
        self.Stocks.append(Stock)

    def setBM(self, Stock):
        BM = Stock


