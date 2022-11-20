import data.stock as st;
import strategy.strategy as strategy;
import numpy as np;

code = '000100'

data = st.getSingleStockPrice(code, '20220120', ' 20220401');
data['buy_signal'] = np.where(data.index.weekday == 3, 1, 0);
data['sell_signal'] = np.where(data.index.weekday == 1, -1, 0);
data = strategy.compose_singal(data);
data = strategy.calculate_profit_pct(data);
data = strategy.calculate_cum_prof(data)  # 计算累计收益率

print(data[['close', 'signal', 'profit_pct', 'cum_profit']]);