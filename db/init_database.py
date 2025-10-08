#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
用于连接MySQL数据库并初始化所有表
"""

import os
import sys
import logging
import mysql.connector
# 导入mysql.connector模块中的Error类
# Error类用于处理与MySQL数据库连接和操作过程中可能出现的错误
from mysql.connector import Error
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('db_init.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def get_db_config():
    """获取数据库配置"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'port': int(os.getenv('DB_PORT', 3306)),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4')
    }

def create_database_and_tables():
    """创建数据库和表"""
    db_config = get_db_config()
    db_name = os.getenv('DB_NAME', 'stock_analysis')

    try:
        # 连接到MySQL服务器（不指定数据库）
        logger.info(f"正在连接到MySQL服务器: {db_config['host']}")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # 创建数据库
        logger.info(f"正在创建数据库: {db_name}")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        logger.info(f"数据库 {db_name} 创建成功")

        # 切换到新创建的数据库
        cursor.execute(f"USE {db_name};")

        # 读取schema.sql文件并执行
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        logger.info(f"正在读取schema文件: {schema_path}")

        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # 执行SQL语句
        logger.info("正在执行SQL语句创建表...")
        statements = schema_sql.split(';')

        for statement in statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                    logger.info(f"执行成功: {statement[:50]}...")
                except Error as e:
                    if e.errno == 1050:  # 表已存在
                        logger.info(f"表已存在，跳过: {statement[:50]}...")
                    else:
                        logger.error(f"执行SQL语句出错: {e}")
                        logger.error(f"出错的SQL: {statement}")

        # 提交事务
        conn.commit()
        logger.info("所有表创建成功")

    except Error as e:
        logger.error(f"数据库操作出错: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.info("数据库连接已关闭")

    return True

def main():
    """主函数"""
    logger.info("开始初始化数据库...")

    if create_database_and_tables():
        logger.info("数据库初始化完成")
        return 0
    else:
        logger.error("数据库初始化失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
