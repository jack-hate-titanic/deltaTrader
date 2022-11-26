"""
Author: 悦者生存 1002783067@qq.com
Date: 2022-05-17 22:29:17
LastEditors: 悦者生存 1002783067@qq.com
LastEditTime: 2022-05-21 10:36:47
FilePath: /python/deltaTrader/data/stock.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""
# 参考地址 https://github.com/Delta-F/DeltaTrader/blob/master/data/stock.py
import os.path

import efinance as ef;
import pandas as pd;
import datetime;

# 设置行列不忽略
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

# 全局变量
data_root = '/Users/wson/Desktop/Trader/data/';


def get_stock_list():
    """
    # 获取所有A股股票代码
    :return
    """
    # 将所有股票列表转换成数组
    stock_list = ef.stock.get_realtime_quotes(['深A']);
    stock_list = handle_data(stock_list);
    return stock_list['code'];


def get_single_stock_price(code, start_time=None, end_time=None):
    """
    # 获取单个股票行情
    :param code 股票代码
    :param end_time 获取股票结束时间
    :param start_time 获取股票开始时间
    :return
    """
    # 时间转化
    if start_time:
        start_time = start_time.replace('-', '');
    if end_time:
        end_time = end_time.replace('-', '');
    # 如果start_time为None的话，那么为上市开始时间
    if start_time is None and end_time is None:
        data = ef.stock.get_quote_history(code);
    elif end_time is None and start_time:
        end_time = datetime.datetime.today();
        data = ef.stock.get_quote_history(code, start_time, end_time);
    else:
        data = ef.stock.get_quote_history(code, start_time, end_time);
    data = handle_data(data);
    return data;


def export_stock_data(data,  filename, type, mode=None):
    # 导出股票行情
    file_root = '/Users/wson/Desktop/Trader/data/' + type + '/' + filename + '.csv';
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


def update_daily_price(stock_code, type ='price'):
    # 是否存在文件：不存在-重新获取， 存在
    file_root = data_root + type + '/' + stock_code + '.csv';
    # 如果存在对应文件
    if os.path.exists(file_root):
        startdate = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1];
        print(startdate+'这是');
        df = get_single_stock_price(stock_code, startdate, datetime.datetime.today().strftime('%Y%m%d'));
        export_stock_data(df, stock_code, 'price', 'a');
    else:
        # 重新获取该股票行情数据
        df = get_single_stock_price(stock_code);
        export_stock_data(df, stock_code, 'price');
    print('数据已经更新成功', stock_code);


def get_csv_price(code, start_date, end_date, columns=None):
    """
    获取本地数据，且顺便完成数据更新工作
    :param code: str,股票代码
    :param start_date: str,起始日期
    :param end_date: str,起始日期
    :param columns: list,选取的字段
    :return: dataframe
    """
    # 使用update直接更新
    update_daily_price(code);
    # 读取数据
    file_root = data_root + 'price/' + code + '.csv';
    if columns is None:
        data = pd.read_csv(file_root, index_col='date');
    else:
        data = pd.read_csv(file_root, usecols=columns, index_col='date')
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)];


def handle_data(data):
    # 数据转化
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
