import pandas as pd;
import numpy as np;
import talib;
import strategy.base as strat;

def boll_strategy(data):
    """
    macd策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :return:
    """
    data = pd.DataFrame(data);
    data['upper'], data['middle'], data['lower'] = talib.BBANDS(data['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0);

    # # 生成信号：金叉买入、死叉卖出
    # data['buy_signal'] = np.where(data['diff'] > data['dea'], 1, 0)
    # data['sell_signal'] = np.where(data['diff'] < data['dea'], -1, 0)
    print(data[['close', 'upper', 'middle', 'lower']])
    #
    # # 过滤信号：st.compose_signal
    # data = strat.compose_signal(data)
    # data = data[data['signal'] != 0]
    # print(data[['close', 'signal']])
    #
    # # 计算单次收益
    # data = strat.calculate_profit_pct(data)
    # # print(data.describe())
    #
    # # 计算累计收益
    # data = strat.calculate_cum_prof(data)
    #
    # # 删除多余的columns
    # data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    #
    # # 数据预览
    # print(data[['close', 'short_ma', 'long_ma', 'signal', 'cum_profit']])

    # return data;