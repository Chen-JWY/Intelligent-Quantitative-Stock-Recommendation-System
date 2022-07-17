from kernal import *

SLib = StockLib()

def init():
    timedelta = '1d'
    starttime = '2021-01-01'
    ibm = Stock('IBM',timedelta,starttime)
    spy = Stock('SPY',timedelta,starttime)
    SLib.addstock(ibm)
    SLib.addstock(spy)
    SLib.setBM(spy)


def main():
    init()
    ibm.MACD.setcash(100000)
    ibm.MACD.test(ibm.bar,starttime,'')
    print(ibm.MACD.Cash)
    ibm.MACD.show(ibm.bar,spy.bar)

if __name__ == '__main__':
    main()
