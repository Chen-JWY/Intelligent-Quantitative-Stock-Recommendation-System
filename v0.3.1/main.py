from kernal import *

timedelta = '1d'
starttime = '2019-01-01'
endtime = '2021-01-01'
now = '20' + dt.datetime.now().strftime('%y-%m-%d')
SLib = StockLib()

def init():
    SLib.addstock(Stock('AAPL', timedelta, starttime, now))
    # SLib.addstock(Stock('TSLA', timedelta, starttime, now))
    # SLib.addstock(Stock('IBM', timedelta, starttime, now))
    SLib.setBM(Stock('SPY', timedelta, starttime, now))

def main():
    init()
    for stock in SLib.Stocks:
        obj = stock.MACD
        obj.setlen(15, 60)  # set parameters of MACD
        obj.setcash(100000)  # 100000USD for each stock
        obj.test(stock.bar, starttime, now)  # use default parameter to run MACD
        obj.show(stock.token, stock.bar, SLib.BM.bar, starttime, now, 0)
        obj.traininit(Parameter(5,50,5),Parameter(20,200,5))  # SMA in [5:50:5]; LMA in [20:200:5]
        obj.train(stock.bar, starttime, endtime, 10)  # use past data, train 10 times to find the better parameters
        print(stock.MACD.slen, stock.MACD.llen)  # print the parameters after training
        obj.test(stock.bar, starttime, now)  # use the parameter to test
        obj.show(stock.token, stock.bar, SLib.BM.bar, starttime, now, 0)


if __name__ == '__main__':
    main()
