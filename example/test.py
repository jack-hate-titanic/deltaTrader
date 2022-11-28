import data.stock as st;
import strategy.week_strategy as strategy;
import numpy as np;
import strategy.compare as sh;

data = st.get_csv_price('000100', '2020-01-01', '2020-02-01');
# print(data);