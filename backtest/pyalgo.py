'''
@desc: 使用algotrade 进行数据回测
'''
from pyalgotrade import strategy
from pyalgotrade_tushare import tools, barfeed
from pyalgotrade.technical import ma
import ssl
## 禁止数字证书验证
ssl._create_default_https_context = ssl._create_unverified_context

def safe_round(value, digits):
    if value is not None:
        value = round(value, digits)
    return value

class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info("%s %s" % (bar.getClose(), safe_round(self.__sma[-1], 2)))

# Load the bar feed from the CSV file
instruments = ["000001"]
feeds = tools.build_feed(instruments, 2017, 2018, "histdata")

# Evaluate the strategy with the feed's bars.
myStrategy = MyStrategy(feeds, instruments[0])
myStrategy.run();