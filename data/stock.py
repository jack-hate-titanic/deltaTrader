'''
Author: 悦者生存 1002783067@qq.com
Date: 2022-05-17 22:29:17
LastEditors: 悦者生存 1002783067@qq.com
LastEditTime: 2022-05-21 10:36:47
FilePath: /python/deltaTrader/data/stock.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from jqdatasdk import *;
import pandas as pd;

auth('17310836100', 'Ven38888');
# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)


# 获取所有A股股票代码
def getStockList():
    # 将所有股票列表转换成数组
    stock_list = list(get_all_securities(['stock']).index);
    return stock_list;


# 获取当个股票行情
def getSingleStockPrice(code, timeperiod, start_time, end_time):
    data = get_price(code, start_time, end_time, frequency=timeperiod);
    # 添加涨跌幅
    data['change'] = (data['close'] - data['close'].shift()) / data['close'].shift() * 100;
    data.columns.names = ['date'];
    return data;


# 导出股票行情
def exportStockData(data, filename):
    file_root = '/Users/wson/Desktop/python/deltaTrader/data/price/' + filename + '.csv';
    data.index.names = ['date']
    data.to_csv(file_root);
    print('已成功存储至：', file_root);


# 周期转换
def transferPriceFreq(data, frequency):
    df_trans = pd.DataFrame();
    df_trans['open'] = data['open'].resample(frequency).first();
    df_trans['close'] = data['close'].resample(frequency).last();
    df_trans['high'] = data['high'].resample(frequency).max();
    df_trans['low'] = data['low'].resample(frequency).min();
    return df_trans;
