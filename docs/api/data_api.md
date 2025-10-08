# 数据查询API文档

## 概述

数据查询API提供对股票数据库中各类数据的查询接口，支持按多种条件筛选和获取数据。

## 接口列表

### 1. 获取股票基本信息

**接口描述**：获取股票的基本信息，包括股票代码、名称、市场、行业等。

**请求路径**：`/api/stocks/basic`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 否 | 股票代码，如"000001" |
| stock_name | string | 否 | 股票名称，如"平安银行" |
| market | string | 否 | 市场，如"sz"（深圳）、"sh"（上海） |
| industry | string | 否 | 行业分类 |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为20 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 100,
        "page": 1,
        "page_size": 20,
        "items": [
            {
                "stock_code": "000001",
                "stock_name": "平安银行",
                "market": "sz",
                "industry": "银行",
                "list_date": "1991-04-03",
                "list_status": "上市"
            },
            ...
        ]
    }
}
```

### 2. 获取股票交易数据

**接口描述**：获取指定股票的交易数据，包括开盘价、最高价、最低价、收盘价等。

**请求路径**：`/api/stocks/daily`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为100 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 1000,
        "page": 1,
        "page_size": 100,
        "items": [
            {
                "stock_code": "000001",
                "trade_date": "2023-01-03",
                "open_price": 12.50,
                "high_price": 12.80,
                "low_price": 12.40,
                "close_price": 12.60,
                "change": 0.10,
                "change_ratio": 0.0080,
                "volume": 1000000,
                "amount": 12500000.00
            },
            ...
        ]
    }
}
```

### 3. 获取财务数据

**接口描述**：获取指定股票的财务数据，包括营收、净利润等。

**请求路径**：`/api/stocks/financial`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| report_type | string | 否 | 报告类型，如"annual"（年报）、"quarter"（季报） |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为20 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 20,
        "page": 1,
        "page_size": 20,
        "items": [
            {
                "stock_code": "000001",
                "report_date": "2022-12-31",
                "report_type": "annual",
                "revenue": 15000000000.00,
                "net_profit": 2000000000.00,
                "total_assets": 30000000000.00,
                "total_liabilities": 20000000000.00,
                "equity": 10000000000.00
            },
            ...
        ]
    }
}
```

### 4. 获取主营业务数据

**接口描述**：获取指定股票的主营业务数据。

**请求路径**：`/api/stocks/business`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为20 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 20,
        "page": 1,
        "page_size": 20,
        "items": [
            {
                "stock_code": "000001",
                "report_date": "2022-12-31",
                "business_type": "银行业",
                "business_revenue": 14000000000.00,
                "business_profit": 1800000000.00
            },
            ...
        ]
    }
}
```

### 5. 获取公告数据

**接口描述**：获取指定股票的公告数据。

**请求路径**：`/api/stocks/announcement`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| announcement_type | string | 否 | 公告类型，如"年报"、"季报"等 |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为20 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 50,
        "page": 1,
        "page_size": 20,
        "items": [
            {
                "announcement_id": 1001,
                "stock_code": "000001",
                "announcement_date": "2023-03-15",
                "announcement_type": "年报",
                "announcement_title": "2022年年度报告",
                "announcement_content": "2022年年度报告详细内容..."
            },
            ...
        ]
    }
}
```

### 6. 获取股东数据

**接口描述**：获取指定股票的股东数据。

**请求路径**：`/api/stocks/shareholder`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| shareholder_type | string | 否 | 股东类型，如"流通股东"、"限售股东"等 |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为20 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 30,
        "page": 1,
        "page_size": 20,
        "items": [
            {
                "stock_code": "000001",
                "report_date": "2022-12-31",
                "shareholder_name": "平安集团",
                "shareholder_type": "流通股东",
                "holding_ratio": 0.2534,
                "holding_shares": 50000000
            },
            ...
        ]
    }
}
```

### 7. 获取技术指标数据

**接口描述**：获取指定股票的技术指标数据。

**请求路径**：`/api/stocks/technical`

**请求方法**：GET

**请求参数**：

| 参数名 | 类型 | 是否必填 | 描述 |
|--------|------|----------|------|
| stock_code | string | 是 | 股票代码，如"000001" |
| start_date | string | 否 | 开始日期，格式"YYYY-MM-DD" |
| end_date | string | 否 | 结束日期，格式"YYYY-MM-DD" |
| indicators | string | 否 | 指标列表，逗号分隔，如"ma5,ma10,macd,rsi" |
| page | integer | 否 | 页码，默认为1 |
| page_size | integer | 否 | 每页记录数，默认为100 |

**响应示例**：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "total": 1000,
        "page": 1,
        "page_size": 100,
        "items": [
            {
                "stock_code": "000001",
                "trade_date": "2023-01-03",
                "ma5": 12.45,
                "ma10": 12.30,
                "ma20": 12.15,
                "macd": 0.15,
                "macd_signal": 0.12,
                "macd_hist": 0.03,
                "rsi": 65.5
            },
            ...
        ]
    }
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 数据格式说明

### 日期格式
所有日期参数使用"YYYY-MM-DD"格式，如"2023-01-01"。

### 数值格式
- 价格：保留2位小数，如12.35
- 比率：保留4位小数，如0.1234（表示12.34%）
- 成交量：整数，单位为手
- 成交额：保留2位小数，单位为元
- 股份数量：整数，单位为股
