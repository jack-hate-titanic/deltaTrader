import data.stock as st;
import strategy.kdj_strategy as kdj;

data = st.get_csv_price('000100', '2022-01-01', '2022-12-01');
kdj.kdj_strategy(data);