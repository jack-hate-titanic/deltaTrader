import stock.stock as st;
import datetime;

code = '000001';
the_date = datetime.datetime.now().strftime('%Y-%m-%d')
pre_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
data = st.update_daily_price(code, pre_date);
# data = st.get_all_stock_data()
print(data);