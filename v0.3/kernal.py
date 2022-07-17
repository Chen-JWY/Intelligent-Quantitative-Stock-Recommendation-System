import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn
from numpy import ndarray
from pandas import DataFrame, Series
from pandas.core.generic import NDFrame

class Parameter:
    val = 0
    mnval = 0
    mxval = 0
    def __init__(self, mnval = 0, mxval = 0):
        self.mnval = mnval
        self.mxval = mxval
        self.val = np.random.random_integers(self.mnval, self.mxval)

    def setlimit(self, mnval, mxval):
        self.mnval = mnval
        self.mxval = mxval

    def gen(self):
        self.val = np.random.random_integers(self.mnval, self.mxval)

class Result:
    startCash = 0
    Cash = 0
    Asset = 0
    Share = 0
    Return = 0
    Alpha = 0
    Beta = 0
    Sharpe = 0
    buypoint = []
    sellpoint = []

    def __init__(self):
        pass

    def clear(self):
        self.Asset = self.startCash
        self.Cash = self.startCash
        self.Share = 0
        self.Alpha = 0
        self.Beta = 0
        self.Sharpe = 0
        self.Return = 0
        self.buypoint = []
        self.sellpoint = []

    def cal(self, bar, BMbar):
        self.Return = (self.Asset - self.startCash)/self.startCash
        # x = pd.Series.to_numpy(bar['Close'].pct_change()[1:])
        # y = pd.Series.to_numpy(BMbar['Close'].pct_change()[1:])
        # self.Beta = (np.cov(x,y)[0,1]) / np.var(y)

    def show(self, bar, BMbar, starttime, endtime):
        self.cal(bar, BMbar)
        print('--------------------RESULT---------------------')
        print("startCash:",self.startCash)
        print("Asset:",round(self.Asset,2))
        print("Cash:",round(self.Cash,2))
        print("Share:",round(self.Share,2))
        print("Alpha:",self.Alpha)
        print("Beta:",self.Beta)
        print("Sharpe",self.Sharpe)
        # print("buy:",self.buypoint)
        # print("sell:",self.sellpoint)
        print("Return: {:.2%}".format(self.Return))
        print('-----------------------------------------------')
        bar = bar[pd.to_datetime(starttime)<=bar['Date']]
        plt.clf()
        plt.subplot(2, 1, 1)
        plt.plot(bar['Date'], bar['Close'])
        plt.plot(bar['Date'], bar['SMA'])
        plt.plot(bar['Date'], bar['LMA'])
        plt.ylabel("Price(USD)")
        plt.subplot(2, 1, 2)
        plt.ylabel("Asset(USD)")
        plt.plot(bar['Date'], bar['Asset'])
        plt.tight_layout()
        plt.savefig('./Result/'+dt.datetime.now().strftime('%H%M%S'))



class Strategy(Result,Parameter):
    def __init__(self):
        pass

    def setcash(self, Cash):
        self.startCash = self.Cash = self.Asset = Cash

    def sell(self, time, price, shares):
        # limit
        self.Cash += price * shares
        self.Share -= shares
        sellpoint.append([time,price])

    def buy(self, time, price, shares):
        # limit
        # print("buy: ",time,shares,price)
        self.Cash -= price * shares
        self.Share += shares
        self.buypoint.append([time,price])

    def liquidate(self, time, price):
        self.Cash += self.Share * price
        # print("sell:", time, self.Share, price, self.Cash)
        self.Share = 0
        self.sellpoint.append([time,price])

    def test(self, starttime, endtime):
        pass

    def train(self, starttime, endtime):
        pass


class _MACD(Strategy):
    slen = 0  # best parameter
    llen = 0
    bestAsset = 0
    _slen = Parameter() # train parameter
    _llen = Parameter()
    istrainready = 0
    def __init__(self):
        pass

    def setlen(self, slen=20, llen=60):
        self.slen = slen
        self.llen = llen
    def test(self, bar, starttime, endtime, istrain = 0):
        self.clear()
        if istrain:
            llen = self._llen.val
            slen = self._slen.val
        else:
            llen = self.llen
            slen = self.slen
        for i in range(llen + 1, len(bar)):
            if not (pd.to_datetime(starttime) <= bar.Date[i] <= pd.to_datetime(endtime)):continue
            sma_pre = bar.Close[i - slen:i].mean()
            sma_now = bar.Close[i - slen + 1:i + 1].mean()
            lma_pre = bar.Close[i - llen:i].mean()
            lma_now = bar.Close[i - llen + 1:i + 1].mean()
            bar.loc[i, ['SMA']] = sma_now
            bar.loc[i, ['LMA']] = lma_now
            if self.Share == 0:
                if sma_pre < lma_pre and sma_now > lma_now:
                    self.buy(bar.Date[i], bar.Close[i], self.Cash / bar.Close[i])
            else:
                self.Asset += self.Share * (bar.Close[i] - bar.Close[i - 1])
                if sma_pre > lma_pre and sma_now < lma_now:
                    self.liquidate(bar.Date[i],bar.Close[i])
            bar.loc[i, ['Asset']] = self.Asset
        if istrain and self.Asset > self.bestAsset:
            self.bestAsset = self.Asset
            self.llen = self._llen.val
            self.slen = self._slen.val

    def traininit(self, _slen, _llen):
        self._slen = _slen
        self._llen = _llen
        self.istrainready = 1
        self.bestAsset = -np.inf

    def train(self, bar, starttime, endtime, times):
        if self.istrainready != 1:
            print('Parameter range is not set')
            return
        for i in range(times):
            self._slen.gen()
            self._llen.gen()
            while self._slen.val == self._llen.val:
                self._slen.gen()
                self._llen.gen()
            if self._slen.val>self._llen.val:
                self._slen.val, self._llen.val = self._llen.val, self._slen.val
            self._slen.val *= 5
            self._llen.val *= 5
            self.test(bar, starttime, endtime, 1)

class StrLib():
    MACD = _MACD()

    def __init__(self):
        pass


class Stock(StrLib):
    token = ''
    data = None
    bar = None

    def __init__(self, token, timedelta, starttime, endtime):
        self.token = token
        self.data = yf.Ticker(token)
        starttime = pd.to_datetime(starttime)
        starttime -= pd.to_timedelta('210 days')
        self.bar = self.data.history(interval=timedelta, start=starttime)
        self.bar.to_csv('./' + str(self.token) + '.csv')
        self.bar = pd.read_csv('./' + str(self.token) + '.csv')
        self.bar['Date'] = pd.to_datetime(self.bar['Date'])


class StockLib:
    Stocks = []
    BM = None

    def __init__(self):
        pass

    def addstock(self, Stock):
        self.Stocks.append(Stock)

    def setBM(self, Stock):
        self.BM = Stock


