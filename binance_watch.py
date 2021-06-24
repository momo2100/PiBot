import pandas as pd
import pandas_ta as ta
from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

def get_spot(symbol='BNBUSDT',startdt= "3 day ago UTC",period =Client.KLINE_INTERVAL_15MINUTE):
    stock_symbol = symbol
    start_date = startdt
    time_frame =  period
    # request historical candle (or klines) data
    bars = client.get_historical_klines(stock_symbol, time_frame, start_date, limit=1000)

    df = pd.DataFrame(bars, columns=['datetime', 'open', 'high', 'low', 'close' ,'volume' ,'date_close'
    ,'asset vol' ,'num trade' ,'buy base' ,'buy asset' , 'unuse'])

    df['datetime'] = pd.to_datetime(df['datetime'],unit='ms')
    df = df[['datetime', 'open', 'high', 'low', 'close' ,'volume']]
    df["datetime"] = pd.to_datetime(df["datetime"]) + pd.to_timedelta(7,unit='h')
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])

    df.set_index('datetime', inplace=True)
    df_indy = df.copy()
    df_indy.ta.bbands(length=21, append=True)
    df_indy.ta.ema(length=5,append=True)
    df_indy.ta.ema(length=10,append=True)
    df_indy.ta.macd(append=True,fast=9,slow=12,signal=26)

    return df_indy

def get_spot(symbol='BNBUSDT',startdt= "3 day ago UTC",period =Client.KLINE_INTERVAL_15MINUTE,filename = '',point =''):
    stock_symbol = symbol
    start_date = startdt
    time_frame =  period
    # request historical candle (or klines) data
    bars = client.get_historical_klines(stock_symbol, time_frame, start_date, limit=1000)

    df = pd.DataFrame(bars, columns=['datetime', 'open', 'high', 'low', 'close' ,'volume' ,'date_close'
    ,'asset vol' ,'num trade' ,'buy base' ,'buy asset' , 'unuse'])

    df['datetime'] = pd.to_datetime(df['datetime'],unit='ms')
    df = df[['datetime', 'open', 'high', 'low', 'close' ,'volume']]
    df["datetime"] = pd.to_datetime(df["datetime"]) + pd.to_timedelta(7,unit='h')
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])

    df.set_index('datetime', inplace=True)
    df_indy = df.copy()
    df_indy.ta.bbands(length=21, append=True)
    df_indy.ta.ema(length=5,append=True)
    df_indy.ta.ema(length=10,append=True)
    df_indy.ta.macd(append=True,fast=9,slow=12,signal=26)

    return df_indy

def get_future(symbol='BNBUSDT',startdt= "3 day ago UTC",period =Client.KLINE_INTERVAL_15MINUTE):
    stock_symbol = symbol
    start_date = startdt
    time_frame =  period
    # request historical candle (or klines) data
    bars = client.futures_klines(symbol=stock_symbol, interval=time_frame, since=start_date, limit=1000)

    df = pd.DataFrame(bars, columns=['datetime', 'open', 'high', 'low', 'close' ,'volume' ,'date_close'
    ,'asset vol' ,'num trade' ,'buy base' ,'buy asset' , 'unuse'])

    df['datetime'] = pd.to_datetime(df['datetime'],unit='ms')
    df = df[['datetime', 'open', 'high', 'low', 'close' ,'volume']]
    df["datetime"] = pd.to_datetime(df["datetime"]) + pd.to_timedelta(7,unit='h')
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])

    df.set_index('datetime', inplace=True)
    df_indy = df.copy()
    df_indy.ta.bbands(length=21, append=True)
    df_indy.ta.ema(length=5,append=True)
    df_indy.ta.ema(length=10,append=True)
    df_indy.ta.macd(append=True,fast=9,slow=12,signal=26)

    return df_indy

def get_futuretest(filename = '',point =''):
    df = pd.read_csv('BNB15M_90D.csv')
    df.set_index('datetime', inplace=True)
    if point != '':
        print(df[:point])

    return df

def is_time_to_long(df):
    i = len(df)-1
    if df.iloc[i-1]["close"] > df.iloc[i-1]["EMA_5"]  and df.iloc[i-1]["close"] > df.iloc[i-1]["open"] and df.iloc[i-1]["MACD_7_14_20"] >0 and  df.iloc[i-1]["close"] < df.iloc[i-1]["BBU_20_2.0"]  and got_order == False: 
        return True
    
    return False


def is_time_to_short(df,got_order):
    i = len(df)-1
    if (df.iloc[i-1]["close"] < df.iloc[i-1]["EMA_5"]  or df.iloc[i]["MACD_7_14_20"] < df.iloc[i-1]["MACD_7_14_20"] or not df.iloc[i-1]["MACD_inc"])and got_order: 
        return True
    return False

if __name__ == "__main__":
    got_order = False
    buy_value = 0
    sum_profit = 0
    profitlst= []
    order_cnt = 0
    order_success = 0

    # df_spot_15m = get_spot(symbol='BNBUSDT',startdt='1 day ago UTC',period=Client.KLINE_INTERVAL_15MINUTE)
    df_future_15m = get_spot(symbol='BNBUSDT',startdt='1 day ago UTC',period=Client.KLINE_INTERVAL_15MINUTE)



    print(df_future_15m.iloc[12:13].index.values)
    # print(df_future_15m.tail(5))
    
