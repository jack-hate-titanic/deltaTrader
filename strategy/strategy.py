import data.stock as st;
import numpy as np;
import datetime
import matplotlib.pyplot as plt
import pandas as pd


def calculate_prof_pct(data):
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    data.loc[data['signal'] != 0, 'profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(
        1) * 100
    data = data[data['signal'] == -1]
    return data


def caculate_max_drawdown(data, window):
    # 计算最大回撤
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window, min_periods=1).max()
    # 计算当天的回撤比=(谷值-峰值)/峰值=谷值/峰值-1
    data['daily_dd'] = data['close'] / data['roll_max'] - 1
    # 选取时间周期内最大的回撤比，即最大回撤
    data['max_dd'] = data['daily_dd'].rolling(window, min_periods=1).min()
    return data;


def compose_singal(data):
    # 整合信号
    data['buy_signal'] = np.where((data['buy_signal'] == 1) & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) & (data['sell_signal'].shift(1) == -1), 0,
                                   data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data


def caculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe, stock
    :return: float
    """
    # 公式：sharpe = (回报率的均值 - 无风险利率) / 回报率的标准差
    # daily_return = data['close'].pct_change()  # 演示部分
    daily_return = data['profit_pct']  # 策略应用后
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普：每日收益率 * 252 = 每年收益率
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year

def calculate_cum_prof(data):
    """
    计算累计收益率 1*(1+3%)
    :param data: dataframe
    :return:
    """
    data['cum_profit'] = pd.DataFrame((1 + data['profit_pct'])).cumprod() - 1
    return data


def week_period_strategy(code, timeperiod, start_time, end_time):
    data = st.getSingleStockPrice(code, timeperiod, start_time, end_time);
    data['weekday'] = data.index.weekday;
    # 周四买入
    data['buy_signal'] = np.where(data['weekday'] == 3, 1, 0);
    # 周一卖出
    data['sell_signal'] = np.where(data['weekday'] == 0, -1, 0);
    data = compose_singal(data);
    data = calculate_prof_pct(data)
    data = calculate_cum_prof(data)  # 计算累计收益率
    print(data);


# if __name__ == '__main__':
#     code = '000100.XSHE';
#     # week_period_strategy(code, 'daily', '2022-03-01', datetime.date.today());
#     df = st.getSingleStockPrice(code, 'daily', '2022-03-01', datetime.date.today())
#     df = caculate_max_drawdown(df, 30)
#     print(df[['close', 'roll_max', 'daily_dd', 'max_dd']])
#     df[['daily_dd', 'max_dd']].plot()
#     plt.show();
