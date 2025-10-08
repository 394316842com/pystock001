CREATE DATABASE IF NOT EXISTS stock_analysis 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE stock_analysis;

-- 股票基本信息表 (修正：移除冗余字段)
CREATE TABLE stock_basic (
    stock_code VARCHAR(10) PRIMARY KEY,
    stock_name VARCHAR(50) NOT NULL,
    market VARCHAR(10) NOT NULL,
    industry VARCHAR(50),
    list_date DATE,
    list_status VARCHAR(10),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 交易数据表 (修正：移除 pre_close_price)
CREATE TABLE stock_daily (
    stock_code VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    open_price DECIMAL(10,2) NOT NULL,
    high_price DECIMAL(10,2) NOT NULL,
    low_price DECIMAL(10,2) NOT NULL,
    close_price DECIMAL(10,2) NOT NULL,
    `change` DECIMAL(10,2),          -- 涨跌额
    change_ratio DECIMAL(10,4),   -- 涨跌幅 (0.0123 = 1.23%)
    volume BIGINT,                -- 成交量 (手)
    amount DECIMAL(15,2),         -- 成交额 (元)
    PRIMARY KEY (stock_code, trade_date),
    INDEX idx_date (trade_date),
    INDEX idx_code (stock_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 财报数据表 (优化：添加索引)
CREATE TABLE financial_statement (
    stock_code VARCHAR(10) NOT NULL,
    report_date DATE NOT NULL,
    report_type VARCHAR(20) NOT NULL,
    revenue DECIMAL(15,2),
    net_profit DECIMAL(15,2),
    total_assets DECIMAL(15,2),
    total_liabilities DECIMAL(15,2),
    equity DECIMAL(15,2),
    PRIMARY KEY (stock_code, report_date),
    INDEX idx_report_date (report_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 主营业务数据表 (优化：添加索引)
CREATE TABLE business_main (
    stock_code VARCHAR(10) NOT NULL,
    report_date DATE NOT NULL,
    business_type VARCHAR(50) NOT NULL,
    business_revenue DECIMAL(15,2),
    business_profit DECIMAL(15,2),
    PRIMARY KEY (stock_code, report_date, business_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 公告数据表 (优化：调整字段长度)
CREATE TABLE announcement (
    announcement_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL,
    announcement_date DATE NOT NULL,
    announcement_type VARCHAR(50),
    announcement_title VARCHAR(255) NOT NULL,
    announcement_content TEXT,
    INDEX idx_stock (stock_code),
    INDEX idx_date (announcement_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 股东数据表 (优化：添加索引)
CREATE TABLE shareholder (
    stock_code VARCHAR(10) NOT NULL,
    report_date DATE NOT NULL,
    shareholder_name VARCHAR(100) NOT NULL,
    shareholder_type VARCHAR(50),
    holding_ratio DECIMAL(10,4),  -- 0.1234 = 12.34%
    holding_shares BIGINT,
    PRIMARY KEY (stock_code, report_date, shareholder_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 技术指标表 (优化：添加索引)
CREATE TABLE technical_indicators (
    stock_code VARCHAR(10) NOT NULL,
    trade_date DATE NOT NULL,
    ma5 DECIMAL(10,2),
    ma10 DECIMAL(10,2),
    ma20 DECIMAL(10,2),
    macd DECIMAL(10,2),
    macd_signal DECIMAL(10,2),
    macd_hist DECIMAL(10,2),
    rsi DECIMAL(10,2),
    PRIMARY KEY (stock_code, trade_date),
    INDEX idx_date (trade_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 回测结果表 (优化：添加索引)
CREATE TABLE backtest_results (
    backtest_id INT AUTO_INCREMENT PRIMARY KEY,
    strategy_name VARCHAR(50) NOT NULL,
    stock_code VARCHAR(10) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_capital DECIMAL(15,2) NOT NULL,
    final_value DECIMAL(15,2) NOT NULL,
    total_return DECIMAL(10,4) NOT NULL,  -- 0.1234 = 12.34%
    sharpe_ratio DECIMAL(10,4),
    max_drawdown DECIMAL(10,4),
    INDEX idx_stock (stock_code),
    INDEX idx_date (start_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;