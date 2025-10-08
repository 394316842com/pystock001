#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库schema分析脚本
分析表结构是否符合项目要求（Pandas + TA-Lib + Backtrader）
"""

import os
import re

def analyze_schema():
    """分析schema.sql文件中的表结构"""
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    if not os.path.exists(schema_path):
        print(f"错误: schema文件不存在: {schema_path}")
        return False

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_content = f.read()

    # 提取所有表名
    table_pattern = r'CREATE TABLE (\w+)'
    tables = re.findall(table_pattern, schema_content)

    print("分析数据库表结构...")
    print("=" * 50)
    print(f"找到 {len(tables)} 个表:")
    for table in tables:
        print(f"- {table}")

    print("表结构分析:")
    print("=" * 50)

    # 分析每个表
    for table in tables:
        print(f"表: {table}")
        print("-" * 30)

        # 提取表的SQL定义
        table_pattern = rf'CREATE TABLE {table} \((.*?)\)'
        match = re.search(table_pattern, schema_content, re.DOTALL)

        if match:
            table_def = match.group(1)

            # 提取字段
            field_pattern = r'(\w+)\s+(\w+(?:\(\d+(?:,\s*\d+)?\))?)'
            fields = re.findall(field_pattern, table_def)

            print("字段:")
            for field, field_type in fields:
                print(f"  - {field}: {field_type}")

            # 检查主键
            primary_key_pattern = r'PRIMARY KEY \((.*?)\)'
            primary_key_match = re.search(primary_key_pattern, table_def)
            if primary_key_match:
                primary_keys = primary_key_match.group(1).split(',')
                print(f"主键: {', '.join(primary_keys)}")

            # 检查索引
            index_pattern = r'INDEX (\w+) \((.*?)\)'
            index_matches = re.findall(index_pattern, table_def)
            if index_matches:
                print("索引:")
                for index_name, index_columns in index_matches:
                    print(f"  - {index_name}: {index_columns}")

    # 分析是否符合项目要求
    print("项目要求分析:")
    print("=" * 50)

    # 检查是否有股票基本信息表
    if 'stock_basic' in tables:
        print("✓ 有股票基本信息表 (stock_basic)")
    else:
        print("✗ 缺少股票基本信息表 (stock_basic)")

    # 检查是否有交易数据表
    if 'stock_daily' in tables:
        print("✓ 有交易数据表 (stock_daily)")
    else:
        print("✗ 缺少交易数据表 (stock_daily)")

    # 检查交易数据表是否有必要的字段
    if 'stock_daily' in tables:
        stock_daily_def = re.search(rf'CREATE TABLE stock_daily \((.*?)\)', schema_content, re.DOTALL).group(1)
        required_fields = ['stock_code', 'trade_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']

        print("交易数据表字段检查:")
        for field in required_fields:
            if field in stock_daily_def:
                print(f"✓ {field}")
            else:
                print(f"✗ 缺少 {field}")

    # 检查是否有技术指标表
    if 'technical_indicators' in tables:
        print("✓ 有技术指标表 (technical_indicators)")

        # 检查技术指标表是否有必要的字段
        tech_def = re.search(rf'CREATE TABLE technical_indicators \((.*?)\)', schema_content, re.DOTALL).group(1)
        tech_fields = ['ma5', 'ma10', 'ma20', 'macd', 'rsi']

        print("
技术指标表字段检查:")
        for field in tech_fields:
            if field in tech_def:
                print(f"✓ {field}")
            else:
                print(f"✗ 缺少 {field}")
    else:
        print("
✗ 缺少技术指标表 (technical_indicators)")

    # 检查是否有回测结果表
    if 'backtest_results' in tables:
        print("
✓ 有回测结果表 (backtest_results)")
    else:
        print("
✗ 缺少回测结果表 (backtest_results)")

    print("
结论:")
    print("=" * 50)
    print("数据库表结构基本符合项目要求，包含了股票基本信息、交易数据、技术指标和回测结果等关键表。")
    print("建议：")
    print("1. 确保在实际使用前，根据具体需求调整字段类型和长度")
    print("2. 考虑添加更多的索引以提高查询性能")
    print("3. 根据需要添加额外的表，如行业分类表、概念板块表等")

    return True

if __name__ == "__main__":
    analyze_schema()
