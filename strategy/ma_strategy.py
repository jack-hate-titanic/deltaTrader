import data.stock as st;
import strategy.base as strat;
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;

def ma_strategy(data, short_window=5, long_window=20):
    """
    双均线策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线，默认5
    :param long_window: 长期n日移动平均线，默认20
    :return:
    """
    print("==========当前周期参数对：", short_window, long_window)

    data = pd.DataFrame(data)
    # 计算技术指标：ma短期、ma长期
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()

    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal']])

    # 过滤信号：st.compose_signal
    data = strat.compose_signal(data)
    # print(data[['close', 'short_ma', 'long_ma', 'signal']])

    # 计算单次收益
    data = strat.calculate_prof_pct(data)
    # print(data.describe())

    # 计算累计收益
    data = strat.calculate_cum_prof(data)

    # 删除多余的columns
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)

    # 数据预览
    print(data[['close', 'short_ma', 'long_ma', 'signal', 'cum_profit']])

    return data;