# 忽略不必要的警告
import warnings

warnings.filterwarnings('ignore')
import pandas_datareader.data as web
import pandas as pd
import datetime

import requests_cache
# 设定缓存及过期时间
from matplotlib import pyplot as plt
from mpl_finance import candlestick2_ohlc
import numpy as np

def get_StockData(StockNum):

    start = datetime.datetime(2018, 1, 1)  # 指定开始时间
    end = datetime.datetime.now()  # 指定结束时间
    # 获取股票交易代码为 000001.SZ 的数据
    data = web.DataReader(StockNum, 'yahoo', start, end)
    return data

def get_StockBata_byCache(StockNum):
    """
    很多时候,高频次请求数据容易造成 IP 被 Ban。我们可以合理利用缓存机制,将数据缓存到本地,还
    可以提示数据读取速度。
    :param StockNum: 股票编号
    :return:
    """
    expire_after = datetime.timedelta(days=3)
    session = requests_cache.CachedSession(cache_name='cache', backend='sqlite',
                                           expire_after=expire_after)
    end = datetime.datetime.now()  # 指定结束时间
    start = end - 10 * datetime.timedelta(days=365)  # 10 年前
    # 获取股票交易代码为 000001.SZ 的数据
    df = web.DataReader(StockNum, 'yahoo', start, end, session=session)
    return df

def data_normalization(df):
    """
    数据的归一化
    :param df:
    :return:
    """
    df_min_max = (df - df.min()) / (df.max() - df.min())
    return df_min_max

def draw_K_line(data):
    """
    绘制K线图
    :param data:
    :return:
    """
    # year_2018 = df['2018-01-01':'2018-07-31']
    fig, ax = plt.subplots(figsize=(16, 9))
    candlestick2_ohlc(ax, data.Open, data.High, data.Low,
                      data.Close, width=.5, alpha=.6)
    plt.show()

def Relative_Chages(data):
    """
    绘制相对变化图
    :param data:
    :return:
    """
    data_close = data.Close
    log_change = np.log(data_close) - np.log(data_close.shift(1))
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(log_change, ".-")
    ax.axhline(y=0, color='red', lw=2)
    plt.show()
    fig, ax = plt.subplots(figsize=(30, 9))
    log_change.plot(kind='bar')
    plt.show()

def best_deals(data):
    data_close = data.Close
    short_rolling = data_close.rolling(window=5).mean()
    long_rolling = data_close.rolling(window=15).mean()
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.plot(data_close.index, data_close, label='year_2018_close')
    ax.plot(short_rolling.index, short_rolling, label='5 days rolling')
    ax.plot(long_rolling.index, long_rolling, label='20 days rolling')
    ax.set_xlabel('Date')
    ax.set_ylabel('Closing price (¥)')
    ax.legend(fontsize='large')
    plt.show()

    fig, ax = plt.subplots(figsize=(16, 9))
    short_long = np.sign(short_rolling - long_rolling)
    buy_sell = np.sign(short_long - short_long.shift(1))
    buy_sell.plot(ax=ax)
    ax.axhline(y=0, color='red', lw=2)
    plt.show()

if __name__ == '__main__':
    StockNum = '000001.SZ'
    # print(get_StockData(StockNum))
    df = get_StockBata_byCache(StockNum)
    # close = df.Close
    # close.plot(figsize=(16, 9))
    df_min_max = data_normalization(df)
    data = df['2019-10-01':'2020-05-01']
    draw_K_line(data)
    Relative_Chages(data)
    best_deals(data)