import data.stock as st;
import strategy.boll_strategy as boll;

data = st.get_csv_price('000100', '2022-01-01', '2022-12-01');
boll.boll_strategy(data);