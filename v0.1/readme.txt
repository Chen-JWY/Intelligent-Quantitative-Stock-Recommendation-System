关键概念：
cash：现金
buy/sell point：买卖记录
s/l len：MACD窗口长度
Securities：个人股票持有数
stocks：股票token表
porp：投资比例（与stocks下标对应，可考虑合并为一个数据结构）
init()：读数据
buy()：买入
sell()：卖出
liquidate()：变现
strategy()：策略，目前MACD，后续会考虑使用strategy类存放每种策略，每种策略单独开设子类
plot()：画图

实现功能：
读入全部有关数据，simple MACD自动买卖，初步可视化

bug：
买入的porp那里逻辑不对，下版本改

下版本可能的更新方向：
显示新闻及公司信息、显示更多参数（如alpha、beta，需要引进benchmark）
