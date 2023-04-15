import stock.stock as stock;
import week_strategy.strategy as strategy;
import pandas as pd;
from matplotlib import pyplot as plot;


def compare_sharpe_ratio(codes=[], start_time='20180101', end_time="20220101"):
    # 获取三只股票的年华夏普比率
    sharpes = [];
    for code in codes:
        data = stock.getSingleStockPrice(code, start_time, end_time);
        sharpe, sharpe_year = strategy.caculate_sharpe(data);
        sharpes.append([code, sharpe_year]);
    # 把夏普比率和code存入dataframe中
    df = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code');
    # 可视化夏普比率
    df.plot.bar(title="sharpe");
    plot.xticks(rotation=30);
    plot.show();