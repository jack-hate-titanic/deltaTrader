import data.stock as st;
import strategy.strategy_model as model;

code = '000001';
data = model.macd_strategy(code, '2022-10-01');
print(data);