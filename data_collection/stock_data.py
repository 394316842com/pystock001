import akshare as ak
import pandas as pd
from db.db_connection import get_db_connection
from datetime import datetime, timedelta
import numpy as np

def get_stock_daily_data(stock_code, start_date, end_date):
    """获取股票日线数据（优化：处理 AkShare 返回格式）"""
    # 获取数据
    df = ak.stock_zh_a_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq"  # 前复权
    )
    
    # 验证数据完整性
    if df.empty:
        raise ValueError(f"No data found for {stock_code} from {start_date} to {end_date}")
    
    # 处理列名（AkShare 返回列名可能变化）
    column_mapping = {
        '日期': 'trade_date',
        '开盘': 'open_price',
        '最高': 'high_price',
        '最低': 'low_price',
        '收盘': 'close_price',
        '成交量': 'volume',
        '成交额': 'amount',
        '涨跌幅': 'change_ratio',
        '涨跌额': 'change'
    }
    
    # 重命名列
    df = df.rename(columns=column_mapping)
    
    # 日期格式转换
    df['trade_date'] = pd.to_datetime(df['trade_date']).dt.date
    
    # 数值处理（处理 AkShare 返回的字符串类型）
    for col in ['change_ratio', 'change', 'open_price', 'high_price', 'low_price', 'close_price', 'volume', 'amount']:
        if df[col].dtype == object:
            # 移除百分号并转为数值
            df[col] = df[col].str.replace('%', '').astype(float) if '%' in df[col].iloc[0] else df[col].astype(float)
    
    # 修正涨跌幅（AkShare 返回的百分比是字符串，需转为小数）
    if 'change_ratio' in df.columns:
        df['change_ratio'] = df['change_ratio'] / 100.0
    
    # 修正成交量（AkShare 返回单位是"手"，需要转为股数？但通常保持原单位）
    # 实际上，AkShare 返回的成交量单位是"手"（1手=100股），但这里我们按原单位存储
    df['volume'] = df['volume'].astype(int)
    
    # 按日期排序
    df = df.sort_values('trade_date').reset_index(drop=True)
    
    # 确保所有字段类型正确
    df = df.astype({
        'open_price': 'float',
        'high_price': 'float',
        'low_price': 'float',
        'close_price': 'float',
        'change': 'float',
        'change_ratio': 'float',
        'volume': 'int',
        'amount': 'float'
    })
    
    return df

def save_stock_daily_data(df, stock_code):
    """安全保存交易数据（优化：处理数据冲突）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查已有数据（使用交易日期）
    cursor.execute("SELECT MAX(trade_date) FROM stock_daily WHERE stock_code = %s", (stock_code,))
    last_date = cursor.fetchone()[0]
    
    # 只插入新数据
    if last_date:
        new_data = df[df['trade_date'] > last_date]
    else:
        new_data = df
    
    if new_data.empty:
        print(f"No new data to insert for {stock_code}")
        cursor.close()
        conn.close()
        return
    
    # 插入数据
    sql = """
    INSERT INTO stock_daily (stock_code, trade_date, open_price, high_price, low_price, 
                           close_price, change, change_ratio, volume, amount)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # 批量插入
    data_to_insert = [
        (
            stock_code,
            row['trade_date'],
            row['open_price'],
            row['high_price'],
            row['low_price'],
            row['close_price'],
            row['change'],
            row['change_ratio'],
            row['volume'],
            row['amount']
        ) for _, row in new_data.iterrows()
    ]
    
    cursor.executemany(sql, data_to_insert)
    conn.commit()
    
    print(f"Inserted {len(new_data)} new records for {stock_code}")
    cursor.close()
    conn.close()