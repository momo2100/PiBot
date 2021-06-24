from binance.client import Client
import pandas as pd
import pandas_ta as ta
import config
import trade_logic

client = Client(config.API_KEY, config.API_SECRET)

def save_future(symbol='BNBUSDT',startdt= "3 day ago UTC",period =Client.KLINE_INTERVAL_15MINUTE):
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
    df_indy.ta.ema(length=8,append=True)
    df_indy.ta.ema(length=20,append=True)
    df_indy.ta.rsi(length=8,append=True)
    df_indy.ta.rsi(length=20,append=True)
    df_indy.ta.variance(length=15,append=True)
    df_indy.ta.macd(append=True,fast=7,slow=15,signal=20)

    return df_indy

def get_futuretest(filename = ''):
    df = pd.read_csv(filename)
    df.set_index('datetime', inplace=True)
    
    return df


if __name__ == "__main__":
    symbol = 'BNBUSDT'
    ### For load data test
    df =save_future(symbol,startdt='30 day ago UTC',period=Client.KLINE_INTERVAL_15MINUTE)
    df.to_csv(symbol+'15M.csv',mode='w')

    df_indy = get_futuretest(filename = symbol+'15M.csv')
    # print(df_indy[df_indy["close"] > df_indy["EMA_8"]] )
    got_order = 'empty'
    buy_value = 0
    sell_value = 0
    profit_lst =[]
    profit = 0
    order_cnt =0
    success_cnt = 0

    for i in range(25,len(df_indy)):
        sign= trade_logic.test_signal(df_indy.iloc[i-5:i])
        # print("sign = [{}] and status = [{}]".format(sign,got_order))
        if sign == 'OPEN BUY' : 
            if got_order == 'SELL' :
                buy_value = df_indy.iloc[i]["close"]
                print("{} CLOSE SELL at {}".format(df_indy.iloc[i].name,buy_value))
                print("\tProfit =  {:.2f}".format(sell_value-buy_value))
                profit += sell_value-buy_value
                profit_lst.append(sell_value-buy_value)
                if sell_value-buy_value > 0 :
                    success_cnt +=1
                got_order = 'empty'
                buy_value,sell_value = 0,0
            #  close sell then open buy
            if got_order != 'BUY' :
                got_order = 'BUY'
                buy_value = df_indy.iloc[i]["close"]
                print("{} OPEN BUY at {}".format(df_indy.iloc[i].name,buy_value))
                order_cnt += 1
        elif sign == 'OPEN SELL' : 
            if got_order == 'BUY' :
                sell_value = df_indy.iloc[i]["close"]
                print("{} CLOSE BUY at {}".format(df_indy.iloc[i].name,sell_value))
                print("\tProfit =  {:.2f}".format(sell_value-buy_value))
                profit += sell_value-buy_value
                profit_lst.append(sell_value-buy_value)
                if sell_value-buy_value > 0 :
                    success_cnt +=1
                got_order = 'empty'
                buy_value,sell_value = 0,0
            #  close buy then open sell
            if got_order != 'SELL' :
                got_order = 'SELL'
                sell_value = df_indy.iloc[i]["close"]
                print("{} OPEN SELL at {}".format(df_indy.iloc[i].name,sell_value))
                order_cnt += 1
        elif sign == 'CLOSE BUY'and got_order == 'BUY' :
            sell_value = df_indy.iloc[i]["close"]
            print("{} CLOSE BUY at {}".format(df_indy.iloc[i].name,sell_value))
            print("\tProfit =  {:.2f}".format(sell_value-buy_value))
            profit += sell_value-buy_value
            profit_lst.append(sell_value-buy_value)
            if sell_value-buy_value > 0 :
                success_cnt +=1
            got_order = 'empty'
            buy_value,sell_value = 0,0
        elif sign == 'CLOSE SELL'and got_order == 'SELL' :
            buy_value = df_indy.iloc[i]["close"]
            print("{} CLOSE SELL at {}".format(df_indy.iloc[i].name,buy_value))
            print("\tProfit =  {:.2f}".format(sell_value-buy_value))
            profit += sell_value-buy_value
            profit_lst.append(sell_value-buy_value)
            if sell_value-buy_value > 0 :
                success_cnt +=1
            got_order = 'empty'
            buy_value,sell_value = 0,0

    if order_cnt > 0 and success_cnt > 0:
        print("\n\n ---------------- Backtest of {}".format(symbol))
        print("Total order {} win {} [{:.2f}]".format(order_cnt,success_cnt,(success_cnt/order_cnt)*100))
        print("MAX profit  {:.2f}  MIN profit {:.2f} and Avg Profit {:.2f}".format(max(profit_lst),min(profit_lst),sum(profit_lst)/len(profit_lst)))
        print("Total profit  {:.2f}".format(profit))

