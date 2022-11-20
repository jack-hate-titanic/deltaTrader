import data.stock as st;

code = '000100'

data = st.getSingleStockPrice(code, '20220201', ' 20220401');
print(data);