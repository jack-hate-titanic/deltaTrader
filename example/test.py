import data.stock as st;

code = '000100.XSHE'

data = st.getSingleStockPrice(code, 'daily', '2022-04-01', '2022-05-01')
print(data);