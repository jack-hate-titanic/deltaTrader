import data.stock as st;
import strategy.macd_strategy as macd;

data = st.get_csv_price('000100', '2020-01-01', '2022-02-01');
macd.macd_strategy(data);