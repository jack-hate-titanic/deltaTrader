import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))

import stock.stock as st;
import datetime;

# code = '000001';
# the_date = datetime.datetime.now().strftime('%Y-%m-%d')
# pre_date = (datetime.datetime.now() - datetime.timedelta(days=60)).strftime('%Y-%m-%d')
# data = st.update_daily_price(code);
st.get_all_stock_data()
# print(data);