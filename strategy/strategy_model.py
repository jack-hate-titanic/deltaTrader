import data.stock as st;
import numpy as np;
import pandas as pd;
import talib;
import strategy.base as bs;


def week_period_strategy(code, start_time, end_time=None):
    """
    周期策略
    :param end_time:
    :param start_time:
    :param code:
    :return:
    """
    # 首先获取股票数据
    data = st.get_csv_price(code, start_time, end_time);
    # 每周四买入，注意weekday的值为0~6
    data['buy_signal'] = np.where(data.index.weekday == 3, 1, 0);
    # 每周二卖出
    data['sell_signal'] = np.where(data.index.weekday == 1, -1, 0);
    data = bs.compose_signal(data);
    data = bs.calculate_profit_pct(data);
    data = bs.calculate_cum_prof(data)  # 计算累计收益率
    data['cum_profit'] = data['cum_profit']*100;
    bs.show_chart(data[['cum_profit']], code);


def macd_strategy(code, start_time, end_time=None):
    """
    macd策略
    :param end_time:
    :param start_time:
    :param code:
    :return:
    """
    # 首先获取股票数据
    data = st.get_csv_price(code, start_time, end_time);
    data['diff'], data['dea'], data['macd'] = talib.MACD(data['close'], fastperiod=12, slowperiod=26, signalperiod=9);
    data['macd'] *= 2;
    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['diff'] > data['dea'], 1, 0)
    data['sell_signal'] = np.where(data['diff'] < data['dea'], -1, 0)

    # #  过滤信号：st.compose_signal
    data = bs.compose_signal(data)
    # calculate_profit(data, code);
    bs.show_buy_sell_chart(data, code);

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

    # 过滤信号：st.compose_signal
    data = bs.compose_signal(data)
    return data;


def short_strategy(code, start_time, end_time=None):
    """
    短线交易策略
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线，默认5
    :param long_window: 长期n日移动平均线，默认20
    :return:
    """
    data = st.get_csv_price(code, start_time, end_time);
    data = ma_strategy(data, 5, 10);
    # calculate_profit(data, code);
    bs.show_buy_sell_chart(data, code);

def calculate_profit(data, code):
    """
    计算收益率
    :param data: dataframe, 投资标的行情数据（必须包含收盘价）
    :param code: 股票代码
    :return:
    """
    # 计算收益率
    data = bs.calculate_profit_pct(data);
    # 计算累计收益率
    data = bs.calculate_cum_prof(data);
    data['cum_profit'] = data['cum_profit'] * 100;
    print(data);
    bs.show_chart(data, code);



