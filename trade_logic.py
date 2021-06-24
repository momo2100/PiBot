import pandas as pd

def have_order():
    return False

def test_signal(df):
    signal_test= ''
    df_len = len(df)

    # print(df.tail(1))
    # print(df.iloc[df_len-1]["close"])

    up1= df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["EMA_8"]
    up2_over_bb = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["BBU_21_2.0"]
    down1_under_bb = df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["BBU_21_2.0"]
    down1= df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["EMA_8"]
    down2= df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and df.iloc[df_len-2]["close"] > df.iloc[df_len-1]["open"]
    ten_gap = (df.iloc[df_len-1]["BBU_21_2.0"] - df.iloc[df_len-1]["BBL_21_2.0"]) > 12
    
    if up1==True and df.iloc[df_len-1]["RSI_8"] < 45 and ten_gap == True:
        signal_test= 'OPEN BUY'
    elif down1 ==True :
        signal_test= 'CLOSE BUY'
    elif down2 == True and df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["BBM_21_2.0"] and ten_gap == True:
        signal_test= 'OPEN SELL'
    elif up1==True :
        signal_test= 'CLOSE SELL'
    elif up2_over_bb == True and down1_under_bb ==True:
        signal_test= 'OPEN SELL'
    elif up1==True and df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["BBM_21_2.0"] and ten_gap == True:
        signal_test= 'OPEN BUY'
    
    return signal_test