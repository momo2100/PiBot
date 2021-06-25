from numpy import sign
import pandas as pd
import pandas_ta as ta
from binance.client import Client
import config
import lineNotify
from datetime import datetime 
import mplfinance as mpf
import trade_logic

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

    df["75"] = 75
    df["25"] = 25

    df.set_index('datetime', inplace=True)
    df_indy = df.copy()
    df_indy.ta.bbands(length=21, append=True)
    df_indy.ta.ema(length=8,append=True)
    df_indy.ta.ema(length=20,append=True)
    df_indy.ta.rsi(length=8,append=True)
    df_indy.ta.rsi(length=20,append=True)
    df_indy.ta.variance(length=15,append=True)
    df_indy.ta.macd(append=True,fast=7,slow=15,signal=20)

    return df,df_indy

def plotfig_15m(df,df_indy,figname="BNBUSDT",sign=''):
    period_u = df_indy[-1:].index.values[0] -pd.Timedelta('20 hours')
    period_d = df_indy[-1:].index.values[0] -pd.Timedelta('0 hours')

    df_indy_plot=df_indy.loc[period_u:period_d]
    df_plot = df.loc[period_u:period_d]

    ap0 = [ mpf.make_addplot(df_indy_plot['BBU_21_2.0'],color='limegreen'),
            mpf.make_addplot(df_indy_plot['BBM_21_2.0'],color='orchid'),   
            mpf.make_addplot(df_indy_plot['BBL_21_2.0'],color='tomato'), 
            mpf.make_addplot(df_indy_plot['EMA_8'],color='maroon', alpha=0.7 ), 
            mpf.make_addplot(df_indy_plot['EMA_20'],color='chocolate', alpha=0.7), 
            mpf.make_addplot(df_indy_plot['75'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='r', alpha=0.25),
            mpf.make_addplot(df_indy_plot['25'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='g', alpha=0.25), 
            mpf.make_addplot(df_indy_plot['RSI_8'],color='lightskyblue',panel=2,ylabel='RSI'),  # panel 2 specified
            mpf.make_addplot(df_indy_plot['RSI_20'],color='brown',panel=2),
        ]
    mpf.plot(df_plot,type='candle', title=figname+' [15M] :'+ datetime.now().strftime("%d/%m/%Y %H:%M") +' "'+sign+'" ', style='yahoo',
            addplot=ap0  ,volume=True, panel_ratios=(2, 0.5, 0.5),figratio=(5,3),
            datetime_format='%H:%M',
            fill_between=dict(y1=df_indy_plot['BBL_21_2.0'].values, 
            y2=df_indy_plot['BBU_21_2.0'].values, 
            color='paleturquoise', alpha=0.20)
            ,scale_width_adjustment=dict(lines=0.5)
            ,savefig=dict(fname=figname+'_15M.png',dpi=100,pad_inches=0.25))

def plotfig_1d(df,df_indy,figname="BNBUSDT",sign=''):
    period_u = df_indy[-1:].index.values[0] -pd.Timedelta('45 days')
    period_d = df_indy[-1:].index.values[0] -pd.Timedelta('0 hours')

    df_indy_plot=df_indy.loc[period_u:period_d]
    df_plot = df.loc[period_u:period_d]

    ap0 = [ mpf.make_addplot(df_indy_plot['BBU_21_2.0'],color='limegreen'),
            mpf.make_addplot(df_indy_plot['BBM_21_2.0'],color='orchid'),   
            mpf.make_addplot(df_indy_plot['BBL_21_2.0'],color='tomato'), 
            mpf.make_addplot(df_indy_plot['EMA_8'],color='maroon', alpha=0.7 ), 
            mpf.make_addplot(df_indy_plot['EMA_20'],color='chocolate', alpha=0.7), 
            mpf.make_addplot(df_indy_plot['75'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='r', alpha=0.25),
            mpf.make_addplot(df_indy_plot['25'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='g', alpha=0.25), 
            mpf.make_addplot(df_indy_plot['RSI_8'],color='lightskyblue',panel=2,ylabel='RSI'),  # panel 2 specified
            mpf.make_addplot(df_indy_plot['RSI_20'],color='brown',panel=2),
        ]
    mpf.plot(df_plot,type='candle', title=figname+' [1D] :'+ datetime.now().strftime("%d/%m/%Y %H:%M") +' "'+sign+'" ', style='yahoo',
            addplot=ap0  ,volume=True, panel_ratios=(2, 0.5, 0.5),figratio=(5,3),
            datetime_format='%d-%B',
            fill_between=dict(y1=df_indy_plot['BBL_21_2.0'].values, 
            y2=df_indy_plot['BBU_21_2.0'].values, 
            color='paleturquoise', alpha=0.20)
            ,scale_width_adjustment=dict(lines=0.5)
            ,savefig=dict(fname=figname+'_1D.png',dpi=100,pad_inches=0.25))

def plotfig_4h(df,df_indy,figname="BNBUSDT",sign=''):
    period_u = df_indy[-1:].index.values[0] -pd.Timedelta('10 days')
    period_d = df_indy[-1:].index.values[0] -pd.Timedelta('0 hours')

    df_indy_plot=df_indy.loc[period_u:period_d]
    df_plot = df.loc[period_u:period_d]

    ap0 = [ mpf.make_addplot(df_indy_plot['BBU_21_2.0'],color='limegreen'),
            mpf.make_addplot(df_indy_plot['BBM_21_2.0'],color='orchid'),   
            mpf.make_addplot(df_indy_plot['BBL_21_2.0'],color='tomato'), 
            mpf.make_addplot(df_indy_plot['EMA_8'],color='maroon', alpha=0.7 ), 
            mpf.make_addplot(df_indy_plot['EMA_20'],color='chocolate', alpha=0.7), 
            mpf.make_addplot(df_indy_plot['75'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='r', alpha=0.25),
            mpf.make_addplot(df_indy_plot['25'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='g', alpha=0.25), 
            mpf.make_addplot(df_indy_plot['RSI_8'],color='lightskyblue',panel=2,ylabel='RSI'),  # panel 2 specified
            mpf.make_addplot(df_indy_plot['RSI_20'],color='brown',panel=2),
        ]
    mpf.plot(df_plot,type='candle', title=figname+' [4H] :'+ datetime.now().strftime("%d/%m/%Y %H:%M") +' "'+sign+'" ', style='yahoo',
            addplot=ap0  ,volume=True, panel_ratios=(2, 0.5, 0.5),figratio=(5,3),
            datetime_format='%d-%B %H:%M',
            fill_between=dict(y1=df_indy_plot['BBL_21_2.0'].values, 
            y2=df_indy_plot['BBU_21_2.0'].values, 
            color='paleturquoise', alpha=0.20)
            ,scale_width_adjustment=dict(lines=0.5)
            ,savefig=dict(fname=figname+'_4H.png',dpi=100,pad_inches=0.25))

def plotfig_1h(df,df_indy,figname="BNBUSDT",sign=''):
    period_u = df_indy[-1:].index.values[0] -pd.Timedelta('3 days')
    period_d = df_indy[-1:].index.values[0] -pd.Timedelta('0 hours')

    df_indy_plot=df_indy.loc[period_u:period_d]
    df_plot = df.loc[period_u:period_d]

    ap0 = [ mpf.make_addplot(df_indy_plot['BBU_21_2.0'],color='limegreen'),
            mpf.make_addplot(df_indy_plot['BBM_21_2.0'],color='orchid'),   
            mpf.make_addplot(df_indy_plot['BBL_21_2.0'],color='tomato'), 
            mpf.make_addplot(df_indy_plot['EMA_8'],color='maroon', alpha=0.7 ), 
            mpf.make_addplot(df_indy_plot['EMA_20'],color='chocolate', alpha=0.7), 
            mpf.make_addplot(df_indy_plot['75'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='r', alpha=0.25),
            mpf.make_addplot(df_indy_plot['25'], panel=2, type='line', secondary_y=False, ylim=(0, 100), color='g', alpha=0.25), 
            mpf.make_addplot(df_indy_plot['RSI_8'],color='lightskyblue',panel=2,ylabel='RSI'),  # panel 2 specified
            mpf.make_addplot(df_indy_plot['RSI_20'],color='brown',panel=2),
        ]
    mpf.plot(df_plot,type='candle', title=figname+' [1H] :'+ datetime.now().strftime("%d/%m/%Y %H:%M") +' "'+sign+'" ', style='yahoo',
            addplot=ap0  ,volume=True, panel_ratios=(2, 0.5, 0.5),figratio=(5,3),
            datetime_format='%d-%B %H:%M',
            fill_between=dict(y1=df_indy_plot['BBL_21_2.0'].values, 
            y2=df_indy_plot['BBU_21_2.0'].values, 
            color='paleturquoise', alpha=0.20)
            ,scale_width_adjustment=dict(lines=0.5)
            ,savefig=dict(fname=figname+'_1H.png',dpi=100,pad_inches=0.25))

if __name__ == "__main__":
    # lineNotify.send_alert('Start monitor')
    # print("Currently .... {}".format(datetime.now().strftime("%d/%m/%Y %H:%M")))
    symbol = 'BNBUSDT'
    with open("order_"+symbol+".txt",'r+') as f:
        got_order = f.read()
    
    # -- Period 1 Days------------------------
    df_1D,df_indy_1D = get_future(symbol=symbol,startdt='60 day ago UTC',period=Client.KLINE_INTERVAL_1DAY)
    sign_1D = trade_logic.test_signal(df_indy_1D)
    plotfig_1d(df_1D,df_indy_1D,symbol,sign_1D)
    print("Day signal  = "+sign_1D)

    # -- Period 4H------------------------
    df_4H,df_indy_4H = get_future(symbol=symbol,startdt='15 day ago UTC',period=Client.KLINE_INTERVAL_4HOUR)
    sign_4H = trade_logic.test_signal(df_indy_4H)
    plotfig_4h(df_4H,df_indy_4H,symbol,sign_4H)
    print("4H signal  = "+sign_4H)

    # -- Period 1H------------------------
    df_1H,df_indy_1H = get_future(symbol=symbol,startdt='7 day ago UTC',period=Client.KLINE_INTERVAL_1HOUR)
    sign_1H = trade_logic.test_signal(df_indy_1H)
    plotfig_1h(df_1H,df_indy_1H,symbol,sign_1H)
    print("1H signal  = "+sign_1H)
    
    # -- Period 15 Mins------------------------
    df,df_indy = get_future(symbol=symbol,startdt='1 day ago UTC',period=Client.KLINE_INTERVAL_15MINUTE)
    sign = trade_logic.test_signal(df_indy)
    plotfig_15m(df,df_indy,symbol,sign)
    print("15Min signal  = "+sign)

    with open('tracking_log.txt','a') as f:
        f.write(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\t ["+symbol+"]    ")
        f.write("sign = [{}] and status = [{}]  last price {}\n".format(sign,got_order,client.get_ticker(symbol=symbol)['bidPrice']))

    if sign == 'OPEN BUY' : 
        if got_order == 'SELL' :
            lineNotify.send_pic(symbol+'_15M','BNBUSDT-Close SELL then Open BUY at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        #  close sell then open buy
        if got_order == 'empty' :
            lineNotify.send_pic(symbol+'_15M','BNBUSDT-Open BUY at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        with open("order_"+symbol+".txt",'w') as f:
            f.write("BUY")
    elif sign == 'OPEN SELL' : 
        if got_order == 'BUY' :
            lineNotify.send_pic(symbol+'_15M','BNBUSDT-Close BUY then Open SELL at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        #  close buy then open sell
        if got_order == 'empty' :
            lineNotify.send_pic(symbol+'_15M','BNBUSDT-Open SELL at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        with open("order_"+symbol+".txt",'w') as f:
            f.write("SELL")
    elif sign == 'CLOSE BUY'and got_order == 'BUY' :
        lineNotify.send_pic(symbol+'_15M','BNBUSDT-Close BUY only at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        with open("order_"+symbol+".txt",'w') as f:
            f.write("empty")
    elif sign == 'CLOSE SELL'and got_order == 'SELL' :
        lineNotify.send_pic(symbol+'_15M','BNBUSDT-Close SELL only at {}'.format(client.get_ticker(symbol=symbol)['bidPrice']))
        with open("order_"+symbol+".txt",'w') as f:
            f.write("empty")
    
    with open('syslog.txt','w') as f:
        f.write("Log of V6.0 " +datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
            
