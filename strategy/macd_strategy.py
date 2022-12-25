import pandas as pd
import talib;

def macd_strategy(data):
    """
    macd策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :return:
    """
    df = pd.DataFrame([]);
    df['dif'], df['dea'], df['macd'] = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9);
    df['macd'] *= 2;
    print(df);
    #
    #
    # # 生成信号：金叉买入、死叉卖出
    # data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    # data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # # print(data[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal']])
    #
    # # 过滤信号：st.compose_signal
    # data = strat.compose_signal(data)
    # # print(data[['close', 'short_ma', 'long_ma', 'signal']])
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