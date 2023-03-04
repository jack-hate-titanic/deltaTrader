import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
import datetime;

def show_chart(data, code):
    data = data['cum_profit'];
    data.plot();
    plt.title(code);
    plt.show();

def show_buy_sell_chart(data, code):
    fig, ax = plt.subplots()
    ax.plot(data.index, data['close'])
    plt.title(code);
    buy = data.loc[data['buy_signal'] == 1];
    sell = data.loc[data['sell_signal'] == -1];
    for index, row in buy.iterrows():
        ax.annotate('B', xy=(index, row['close']),
                    arrowprops=dict(facecolor='red', shrink=0.05))
    for index, row in sell.iterrows():

        ax.annotate('S', xy=(index, row['close']),
                    arrowprops=dict(facecolor='green', shrink=0.05))
    plt.show();

def compose_signal(data):
    # 整合信号
    # 只留下buy_signal为1，sell_signal为-1的日期
    data = data.loc[(data['buy_signal'] != 0) | (data['sell_signal'] != 0)]
    # buy_signal 为买入信号，设置为1，如果当前买入信号为1并且前一个买入信号也为1，那么设置当前买入信号为零
    data.loc[(data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 'buy_signal'] = 0
    # sell_signal 为卖出信号，设置为-1，如果当前卖出信号为-1并且前一个卖出信号也为-1，那么设置当前卖出信号为零
    data.loc[(data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 'sell_signal'] = 0
    # signal
    data_copy = data.copy();
    data_copy.loc[:, 'signal'] = data_copy['buy_signal'] + data_copy['sell_signal']
    return data_copy



def calculate_profit_pct(data):
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    # profit 利润
    # percent 百分比
    # 下面这种写法会引起settingWithCopyWarning, 因为你修改数据，会影响原始数据
    # # 只留下有交易信号的数据 筛选
    # data = data[data['signal'] != 0];
    # # 计算收益率  (市价-成本价)/成本价
    # data['profit_pct'] = (data['close']-data['close'].shift(1))/data['close'].shift(1) * 100
    # 修改以后
    data['profit_pct'] = data.loc[data['signal'] != 0, 'close'].pct_change()
    # 获得每一次平仓的收益
    data = data[data['signal'] == -1]
    return data


def calculate_max_drawdown(data, window):
    # 计算最大回撤, 风险指标
    # 选取时间周期(时间窗口window = 2,代表过去两天的)
    # 选取时间周期中的最大净值，就是都是正值
    data['roll_max'] = data['close'].rolling(window=252, min_periods=1).max()
    # 计算当天的回撤比=(谷值-峰值)/峰值=谷值/峰值-1，dd的意思是drawdown
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()
    return data;


def calculate_cum_prof(data):
    """
    计算累计收益率 1*(1+3%)
    :param data: dataframe
    :return:
    """
    data['cum_profit'] = pd.DataFrame((1 + data['profit_pct'])).cumprod() - 1
    return data


def caculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe, stock
    :return: float
    """
    # 公式：sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    # 因子项： 回报率均值 = 日涨跌幅.mean()
    # 因子项： 无风险利率 3%/252
    # 因子项： 回报率的标准差 日涨跌幅.stddeviation()
    # daily_return = data['close'].pct_change()  # 演示部分
    daily_return = data['close'].pct_change()  # 策略应用后
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普：每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year