from kernal import *

def main():
    for id in range(len(stocks)):
        token = stocks[id]
        bar = init(token)
        strategy(id,bar)
        liquidate(token,bar.iloc[-1,4])
    print(cash)
    print(buypoint)
    print(sellpoint)
    plot()


if __name__ == '__main__':
    main()