'''
Author: 悦者生存 1002783067@qq.com
Date: 2022-05-17 22:29:17
LastEditors: 悦者生存 1002783067@qq.com
LastEditTime: 2022-05-21 10:36:47
FilePath: /python/deltaTrader/data/stock.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# 参考地址 https://github.com/Delta-F/DeltaTrader/blob/master/data/stock.py
import efinance as ef;
import pandas as pd;
import datetime;

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)



'''
# 获取所有A股股票代码
:return
'''
def getStockList():
    # 将所有股票列表转换成数组
    stock_list = ef.stock.get_realtime_quotes(['深A']);
    stock_list = handleData(stock_list);
    return stock_list['code'];


'''
# 获取单个股票行情
:param code 股票代码
:param start_time 获取股票开始时间
:param end_time 获取股票结束时间
:return
'''
def getSingleStockPrice(code, start_time = None, end_time = None):
    # 如果start_time为None的话，那么为上市开始时间
    if start_time is None and end_time is None:
        data = ef.stock.get_quote_history(code);
    elif end_time is None and start_time:
        end_time = datetime.datetime.today();
        data = ef.stock.get_quote_history(code, start_time, end_time);
    else:
        data = ef.stock.get_quote_history(code, start_time, end_time);
    data = handleData(data);
    return data;


# 导出股票行情
def exportStockData(data, filename, mode = None):
    file_root = '/Users/wson/Desktop/Trader/data/price/' + filename + '.csv';
    if mode == 'a':
        # 因为是新加入的数据，要排到后面，所以header为false
        data.to_csv(file_root, mode=mode, header=False);
        # 删除重复值
        data = pd.read_csv(file_root);
        # 以日期为准进行删除重复值
        data = data.drop_duplicates(subset=['date']);
        data.sort_values('date');
        data.to_csv(file_root, index=False);
    else:
        data.to_csv(file_root);
    print('已成功存储至：', file_root);


# 数据转化
def handleData(data):
    data.rename(
        columns={
            "股票名称": 'name',
            "股票代码": 'code',
            "日期": 'date',
            "开盘": 'open',
            "收盘": 'close',
            "最高": 'high',
            "最低": "low",
            "涨跌幅": 'close_pct',
            "成交量": 'volume',
            "成交额": 'money'
        },
        inplace=True
    );
    data.index = pd.to_datetime(data['date']);
    return data;