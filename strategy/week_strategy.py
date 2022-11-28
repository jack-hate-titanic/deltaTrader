import data.stock as st;
import numpy as np;
import strategy.base as bs;




def week_period_strategy(code, start_time, end_time):
    data = st.get_single_stock_price(code, start_time, end_time);
    data['buy_signal'] = np.where(data.index.weekday == 3, 1, 0);
    data['sell_signal'] = np.where(data.index.weekday == 1, -1, 0);
    data = bs.compose_singal(data);
    data = bs.calculate_profit_pct(data);
    data = bs.calculate_cum_prof(data)  # 计算累计收益率
    data = bs.calculate_max_drawdown(data, 252) # 计算最大回撤比
    print(data[['close', 'signal', 'profit_pct', 'cum_profit', 'max_dd']]);
    bs.show_chart(data[['cum_profit']])



