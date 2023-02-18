import data.stock as st;

code = '000001';
data = st.get_csv_price(code, '2019-10-20');
print(data);