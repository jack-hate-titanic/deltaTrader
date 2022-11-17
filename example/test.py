import data.stock as st;

code = '000100'

data = st.getSingleStockPrice(code);
st.exportStockData(data, code)
print(data);