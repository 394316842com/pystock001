import backtrader as bt
import pandas as pd
from db.db_connection import get_db_connection
from datetime import datetime

class MovingAverageStrategy(bt.Strategy):
    params = (
        ('ma_period', 20),
    )
    
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.ma_period)
    
    def next(self):
        if self.sma[0] > self.data.close[0] and not self.position:
            self.buy()
        elif self.sma[0] < self.data.close[0] and self.position:
            self.close()

def run_backtest(stock_code, start_date, end_date, strategy_class, initial_capital=100000):
    """安全运行回测（优化：数据验证、异常处理）"""
    # 验证日期
    if start_date > end_date:
        raise ValueError("Start date must be before end date")
    
    # 获取数据
    conn = get_db_connection()
    query = f"""
        SELECT trade_date, open_price, high_price, low_price, close_price, volume, amount
        FROM stock_daily
        WHERE stock_code = '{stock_code}'
        AND trade_date >= '{start_date}'
        AND trade_date <= '{end_date}'
        ORDER BY trade_date
    """
    
    # 验证数据是否存在
    df = pd.read_sql(query, conn)
    if df.empty:
        raise ValueError(f"No data found for {stock_code} in date range {start_date} to {end_date}")
    
    # 创建Cerebro引擎
    cerebro = bt.Cerebro()
    cerebro.addstrategy(strategy_class)
    
    # 添加数据（使用 PandasData）
    data = bt.feeds.PandasData(
        dataframe=df,
        datetime='trade_date',
        open='open_price',
        high='high_price',
        low='low_price',
        close='close_price',
        volume='volume',
        openinterest=None
    )
    cerebro.adddata(data)
    
    # 设置初始资金
    cerebro.broker.setcash(initial_capital)
    
    # 运行回测
    print(f"Starting backtest for {stock_code} from {start_date} to {end_date}")
    cerebro.run()
    
    # 获取结果
    final_value = cerebro.broker.getvalue()
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    # 计算关键指标
    sharpe_ratio = cerebro.broker.get_sharpe_ratio()
    max_drawdown = cerebro.broker.get_max_drawdown()
    
    # 保存结果
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO backtest_results (strategy_name, stock_code, start_date, end_date, 
                                     initial_capital, final_value, total_return, 
                                     sharpe_ratio, max_drawdown)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        strategy_class.__name__,
        stock_code,
        start_date,
        end_date,
        initial_capital,
        final_value,
        total_return,
        sharpe_ratio,
        max_drawdown
    ))
    conn.commit()
    cursor.close()
    
    # 关闭连接
    conn.close()
    
    return {
        'final_value': final_value,
        'total_return': total_return,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown
    }