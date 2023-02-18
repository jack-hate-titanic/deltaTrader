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

# 引入efinance库
import efinance as ef;
import pandas as pd;
import datetime;

# 设置行列不忽略
# pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 1000)

# 全局变量
data_root = '/Users/wson/Desktop/Trader/data/';


def get_stock_list():
    """
    # 获取所有A股股票代码
    :return
    """
    # 将所有股票列表转换成数组
    stock_list = ef.stock.get_realtime_quotes();
    stock_list = handle_data(stock_list);
    return stock_list[['code', 'name']];


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
        data = ef.stock.get_quote_history(code, start_time);
    else:
        data = ef.stock.get_quote_history(code, start_time, end_time);
    data = handle_data(data);
    new_data = data[['name', 'code', 'date', 'open', 'close', 'close_pct', 'volume']]
    return new_data;


def export_stock_data(data,  filename, mode=None):
    """
    :param data: 传入的数据
    :param filename: 文件名：请传入code
    :param mode: to_csv的模式： mode为a是新加入数据，否则就是重新写入
    :return:
    """
    # 导出股票行情
    file_root = data_root + filename + '.csv';
    # 如果mode为a那么就是新添加数据
    if mode == 'a':
        # 因为是新加入的数据，要排到后面，所以header为false
        data.to_csv(file_root, mode=mode, header=False);
        # 删除重复值
        data = pd.read_csv(file_root);
        # 以日期为准进行删除重复值
        data = data.drop_duplicates(subset=['date']);
        data = data.sort_values('date');
        data.to_csv(file_root, index=False);
    # 否则就是重新写入数据
    else:
        data.to_csv(file_root);
    print('已成功存储至：', file_root);


def update_daily_price(stock_code, start_data):
    # 是否存在文件：不存在-重新获取， 存在-获取csv文件中的最后一天，然后请求csv文件中的最后一天到今天的数据，并写入csv文件中
    file_root = data_root + '/' + stock_code + '.csv';
    date_columns_data = pd.read_csv(file_root, usecols=['date']);
    # 如果存在对应文件
    if os.path.exists(file_root):
        # 读取csv文件，并获取csv文件中最后一天的时间
        startdate = date_columns_data['date'].iloc[-1];
        # 请求csv文件中最后一天到今天的数据
        df = get_single_stock_price(stock_code, startdate, datetime.datetime.today().strftime('%Y%m%d'));
        # 添加到csv文件中
        export_stock_data(df, stock_code, 'a');
    else:
        # 重新获取该股票行情数据
        df = get_single_stock_price(stock_code);
        export_stock_data(df, stock_code);
    # 判断start_data是小于csv文件的时间列的第一个值
    csv_start_data = date_columns_data['date'].iloc[0];
    # 转化为时间戳
    if start_data < csv_start_data:
        print("执行了");
        # 请求t1到t2的时间
        df = get_single_stock_price(stock_code, start_data, csv_start_data);
        # 添加到csv文件中
        export_stock_data(df, stock_code, 'a');
    print('数据已经更新成功', stock_code);


def get_csv_price(code, start_date, end_date=None, columns=None):
    """
    获取本地数据，且顺便完成数据更新工作
    :param code: str,股票代码
    :param start_date: str,起始日期
    :param end_date: str,起始日期
    :param columns: list,选取的字段
    :return: dataframe
    """
    # 如果end_date为空的话
    if end_date is None:
        end_date = datetime.datetime.today().strftime('%Y-%m-%d');
    # 使用update直接更新
    update_daily_price(code, start_date);
    # 读取数据
    file_root = data_root + '/' + code + '.csv';
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

    # 如果data中存在date这一列，那么把date设置为索引
    if 'date' in data:
        data.index = pd.to_datetime(data['date']);
    return data;
