'''
Watch only EMA5 
'''
from time import sleep
import pandas as pd
import pandas_ta as ta
from binance.client import Client
import config
import lineNotify
from datetime import datetime

client = Client(config.API_KEY, config.API_SECRET)

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

def chk_signal(df):
    pos = len(df)

    # ถ้า close ก่อนหน้าเป็นแดงและเปิดต่ำกว่า EMA5 และตัวต่อมาเป็นเขียว high แตะ EMA5
    if df.iloc[pos-2]["close"] < df.iloc[pos-2]["open"] and df.iloc[pos-2]["EMA_5"]-df.iloc[pos-2]["close"] >2 and df.iloc[pos-2]["open"] < df.iloc[pos-2]["EMA_5"] and df.iloc[pos-1]["close"] > df.iloc[pos-1]["open"] and df.iloc[pos-1]["high"] > df.iloc[pos-1]["EMA_5"]:
        return 'BUY'
    elif df.iloc[pos-2]["close"] > df.iloc[pos-2]["open"] and df.iloc[pos-2]["open"]-df.iloc[pos-2]["EMA_5"] >2  and df.iloc[pos-2]["open"] > df.iloc[pos-2]["EMA_5"] and df.iloc[pos-1]["close"] < df.iloc[pos-1]["open"] and df.iloc[pos-1]["low"] < df.iloc[pos-1]["EMA_5"]:
        return 'SELL'

if __name__ == "__main__":
    got_order = False
    buy_value = 0
    sum_profit = 0
    profitlst= []
    order_cnt = 0
    order_success = 0

    lineNotify.send_alert('Start monitor')
    print("Currently .... {}".format(datetime.now().strftime("%d/%m/%Y %H:%M")))

    while True:
        df = get_future(symbol='BNBUSDT',startdt='1 day ago UTC',period=Client.KLINE_INTERVAL_15MINUTE)
        sign = chk_signal(df)
        if sign == 'BUY' and not got_order:
            got_order =not got_order
            buy_value = float(client.get_ticker(symbol='BNBUSDT')['bidPrice'])
            order_cnt += 1
            print(f"{i}  ++BUY++ at {buy_value}")
            lineNotify.send_alert('(Logic3) BNBUSDT ++BUY++ at {}'.format(buy_value))
            with open('price','wb') as f:
                f.write('(Logic3) BNBUSDT ++BUY++ at {}'.format(buy_value))
        elif sign == 'SELL' and got_order:
            got_order =not got_order
            sell_value = float(client.get_ticker(symbol='BNBUSDT')['bidPrice'])
            sum_profit += sell_value-buy_value
            profitlst.append(((sell_value-buy_value)/buy_value)*100)
            if sell_value-buy_value > 0 :
                order_success += 1
            
            print(f"{i}  --SELL-- at {sell_value} : take profit {sell_value-buy_value}",end="")
            print(f" [{profitlst[-1]}%]")
            lineNotify.send_alert('(Logic3)BNBUSDT --SELL-- at {} and take profit {}'.format(sell_value,sell_value-buy_value))
            with open('price','wb') as f:
                f.write('(Logic3) BNBUSDT --SELL-- at {} and take profit {}'.format(sell_value,sell_value-buy_value))
        
        if datetime.now().strftime("%M") == '00':
            print("Currently .... {}".format(datetime.now().strftime("%d/%m/%Y %H:%M")))
        sleep(90)
