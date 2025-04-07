import pandas as pd
import akshare as ak

# 1. 获取实时股票行情
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
# print(stock_zh_a_spot_df.head())

# 2. 获取某只股票的历史行情数据
# 使用另一个函数获取历史数据

def get_stock_data(symbol, period, start_date, end_date):
    """
    获取指定股票的历史行情数据
    :param symbol: 股票代码
    :param period: 数据周期（如：daily, weekly, monthly）
    :param start_date: 开始日期（格式：YYYYMMDD）
    :param end_date: 结束日期（格式：YYYYMMDD）
    :return: 股票历史行情数据的DataFrame
    """
    df = ak.stock_zh_a_hist(symbol=symbol, period=period, start_date=start_date, end_date=end_date, adjust="")
    return df
    
def standardize_stock_data(df):
    """
    标准化股票数据
    :param df: 股票数据的DataFrame
    :return: 标准化后的DataFrame，支持日期索引和数值比较
    """
    # 列名映射
    column_mapping = {
        '日期': 'Date',
        '股票代码': 'Stock_Code',
        '开盘': 'Open',
        '收盘': 'Close',
        '最高': 'High',
        '最低': 'Low',
        '成交量': 'Volume',
        '成交额': 'Turnover',
        '振幅': 'Amplitude',
        '涨跌幅': 'Price_Change_Pct',
        '涨跌额': 'Price_Change',
        '换手率': 'Turnover_Rate'
    }

    # 应用列名转换
    df = df.rename(columns=column_mapping)

    # 转换日期为datetime格式
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 确保日期列存在
    if 'Date' not in df.columns:
        raise ValueError("DataFrame must contain a 'Date' column")
    
    # 设置日期为索引以进行时间序列分析
    df_ts = df.set_index('Date')
    
    # 确保索引是DatetimeIndex类型，以支持数值比较
    if not isinstance(df_ts.index, pd.DatetimeIndex):
        raise ValueError("Failed to convert index to DatetimeIndex")
    
    return df_ts



# 使用example：
# df_ts = get_stock_data("601111", "daily", "20000101", "20250407")
# df_ts = standardize_stock_data(df_ts)


