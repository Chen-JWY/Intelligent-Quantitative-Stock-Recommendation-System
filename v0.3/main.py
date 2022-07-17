from kernal import *

timedelta = '1d'
starttime = '2019-01-01'
endtime = '2021-01-01'
now = '20' + dt.datetime.now().strftime('%y-%m-%d')
SLib = StockLib()

def init():
    SLib.addstock(Stock('AAPL', timedelta, starttime, now))
    SLib.addstock(Stock('TSLA', timedelta, starttime, now))
    SLib.addstock(Stock('IBM', timedelta, starttime, now))
    SLib.setBM(Stock('SPY', timedelta, starttime, now))

def main():
    init()
    for stock in SLib.Stocks:
        obj = stock.MACD
        obj.setlen(15, 60)
        obj.setcash(100000)
        obj.test(stock.bar, starttime, now)
        obj.show(stock.bar, SLib.BM.bar, starttime, endtime)
        obj.traininit(Parameter(1,10),Parameter(4,40)) # LMA in [5:50:5]; SMA in [20:200:5]
        obj.train(stock.bar, starttime, endtime, 10)
        print(stock.MACD.slen, stock.MACD.llen)
        obj.test(stock.bar, starttime, now)
        obj.show(stock.bar, SLib.BM.bar, starttime, endtime)


if __name__ == '__main__':
    main()
