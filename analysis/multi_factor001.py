# analysis/multi_factor.py
from abc import ABC, abstractmethod
import pandas as pd
from db.db_connection import get_db_connection
from datetime import datetime

class MultiFactorStrategy(ABC):
    """多因素分析策略基类"""
    
    def __init__(self, stock_code, start_date, end_date):
        self.stock_code = stock_code
        self.start_date = start_date
        self.end_date = end_date
        self.data = None  # 用于存储合并后的数据
    
    @abstractmethod
    def calculate_factors(self):
        """计算多因素指标（子类必须实现）"""
        pass
    
    def load_data(self):
        """加载股票日线数据和财务数据"""
        # 加载日线数据
        conn = get_db_connection()
        query_daily = f"""
            SELECT trade_date, close_price, volume
            FROM stock_daily
            WHERE stock_code = '{self.stock_code}'
            AND trade_date >= '{self.start_date}'
            AND trade_date <= '{self.end_date}'
            ORDER BY trade_date
        """
        df_daily = pd.read_sql(query_daily, conn)
        
        # 加载财务数据（例如，最近一期的财报）
        query_financial = f"""
            SELECT report_date, net_profit, total_assets
            FROM financial_statement
            WHERE stock_code = '{self.stock_code}'
            AND report_date <= '{self.end_date}'
            ORDER BY report_date DESC
            LIMIT 1
        """
        df_financial = pd.read_sql(query_financial, conn)
        
        # 合并数据
        if not df_financial.empty:
            # 用最近的财报数据
            last_report_date = df_financial['report_date'].iloc[0]
            # 将财报数据与日线数据关联（这里简单关联到财报日期的当天）
            df_daily['report_date'] = last_report_date
            df_daily['net_profit'] = df_financial['net_profit'].iloc[0]
            df_daily['total_assets'] = df_financial['total_assets'].iloc[0]
        
        self.data = df_daily
        conn.close()
    
    def run(self):
        """运行多因素分析"""
        self.load_data()
        self.calculate_factors()
        return self.data

class ValueInvestmentStrategy(MultiFactorStrategy):
    """价值投资策略：基于市净率（PB）和市盈率（PE）"""
    
    def calculate_factors(self):
        # 假设我们已经从财务数据中获取了每股净资产（book_value_per_share）和每股收益（eps）
        # 这里我们简化：用总净资产和总股本（但实际需要从财报中获取）
        # 由于我们只有一期财报，我们假设总股本不变
        # 计算市净率 = 当前股价 / (总净资产 / 总股本)
        # 但这里我们没有总股本，所以用总净资产（假设总股本为1，实际需要获取）
        
        # 为演示，我们假设总股本为1亿股
        total_shares = 100000000  # 1亿股
        
        # 计算每股净资产
        if 'total_assets' in self.data.columns:
            self.data['book_value_per_share'] = self.data['total_assets'] / total_shares
        else:
            self.data['book_value_per_share'] = 0.0
        
        # 计算市净率
        self.data['pb_ratio'] = self.data['close_price'] / self.data['book_value_per_share']
        
        # 计算市盈率（需要每股收益，这里假设从财报中获取了eps）
        # 由于我们没有eps，这里用一个固定值模拟
        self.data['eps'] = 1.0  # 模拟
        self.data['pe_ratio'] = self.data['close_price'] / self.data['eps']
        
        # 生成信号：当pb_ratio < 1.5 且 pe_ratio < 20 时，买入
        self.data['signal'] = (self.data['pb_ratio'] < 1.5) & (self.data['pe_ratio'] < 20)