# analysis/backtest.py
from analysis.multi_factor import ValueInvestmentStrategy

def run_multi_factor_backtest(stock_code, start_date, end_date):
    # 创建多因素策略
    strategy = ValueInvestmentStrategy(stock_code, start_date, end_date)
    # 运行策略，获取信号
    signals = strategy.run()
    
    # 然后可以将信号转换为回测信号
    # 例如：当市盈率低于行业平均时买入
    # 这里需要根据信号生成交易指令
    
    # 然后使用backtrader回测
    # ... [类似之前的回测代码] ...