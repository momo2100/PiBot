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

def test_signal_level(df):
    signal_test= ''
    df_len = len(df)
    # follow buy 1 => แท่งล่าสุดเขียว และ หนามากกว่า 1.5 เท่าของแท่งก่อนหน้า
    cnd_follow_buy1 = df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
        (df.iloc[df_len-1]["close"] - df.iloc[df_len-1]["open"]) > (abs(df.iloc[df_len-2]["close"] - df.iloc[df_len-2]["open"])*1.5)
    cnd_follow_sell1 = df.iloc[df_len-1]["open"] > df.iloc[df_len-1]["close"] and \
        (df.iloc[df_len-1]["open"] - df.iloc[df_len-1]["close"]) > (abs(df.iloc[df_len-2]["close"] - df.iloc[df_len-2]["open"])*1.5)

    # follow buy 2 => 3แท่งเขียว ปิดมากกว่าแท่งก่อนหน้า
    cnd_follow_buy2 = df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
        df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
            df.iloc[df_len-3]["close"] > df.iloc[df_len-3]["open"]
    cnd_follow_sell2 = df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
        df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
            df.iloc[df_len-3]["close"] < df.iloc[df_len-3]["open"]

    # follow buy 3 => 2 แท่งสีเดียวกัน หางไม่เกินตัวก่อนหน้า
    cnd_follow_buy3 = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["low"] > df.iloc[df_len-2]["low"]
    cnd_follow_sell3 = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["high"] < df.iloc[df_len-2]["high"]

    # change side to sell ตรงกลาง =>  แท่งก่อนหน้าเขียว แท่งล่าสุดแดง เส้น bbบนหักลง (BBU1 < BBU2) และ BBM อยู่ระหว่าง hi low แท่งสุดท้าย
    ch2sell = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-2]["BBU_21_2.0"] > df.iloc[df_len-1]["BBU_21_2.0"] and \
                df.iloc[df_len-1]["low"] < df.iloc[df_len-1]["BBM_21_2.0"] < df.iloc[df_len-1]["high"]

    # change side to buy ตรงกลาง =>  แท่งก่อนหน้าแดง แท่งล่าสุดเขียว เส้น bbล่างหักขึ้น (BBL1 > BBL2) และ BBM อยู่ระหว่าง hi low แท่งสุดท้าย
    ch2buy = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["BBL_21_2.0"] > df.iloc[df_len-2]["BBL_21_2.0"] and \
                df.iloc[df_len-1]["low"] < df.iloc[df_len-1]["BBM_21_2.0"] < df.iloc[df_len-1]["high"]

    # turn to buy จุดล่าง => แท่งก่อนหน้าเป็นแดง เปิดต่ำกว่า EMA_8 ปิดต่ำกว่า BBL และ RSI_8 ต่ำกว่า40 แท่งต่อมาเป็นเขียว ไส้ยาวกว่าแท่งก่อนหน้า EMA_8 < BBM
    turn2buy100 = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["open"] < df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["BBL_21_2.0"] and \
                df.iloc[df_len-1]["RSI_8"] <= 40 and \
                    df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
                        (df.iloc[df_len-1]["high"] - df.iloc[df_len-1]["low"]) > (df.iloc[df_len-2]["high"] - df.iloc[df_len-2]["low"]) and \
                            df.iloc[df_len-2]["EMA_8"] < df.iloc[df_len-2]["BBM_21_2.0"]
    
    # turn to sell จุดบน => แท่งก่อนหน้าเป็นเขียว เปิดสูงกว่า EMA_8 ปิดสูงกว่า BBU และ RSI_8 สูงกว่า60 แท่งต่อมาเป็นแดง ไส้ยาวกว่าแท่งก่อนหน้า EMA_8 > BBM
    turn2sell100 = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["open"] > df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["BBU_21_2.0"] and \
                df.iloc[df_len-1]["RSI_8"] >= 60 and \
                    df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
                        (df.iloc[df_len-1]["high"] - df.iloc[df_len-1]["low"]) > (df.iloc[df_len-2]["high"] - df.iloc[df_len-2]["low"]) and\
                            df.iloc[df_len-2]["EMA_8"] > df.iloc[df_len-2]["BBM_21_2.0"]
     
    # turn to buy จุดล่าง(แค่ไส้ทะลุ) => แท่งก่อนหน้าเป็นแดง เปิดต่ำกว่า EMA_8 แท่งต่อมาเป็นเขียว low ต่ำกว่า BBL ปิดสูงกว่าตัวที่แล้ว EMA_8 < BBM
    turn2buy50 = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["open"] < df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
                df.iloc[df_len-1]["low"] < df.iloc[df_len-1]["BBL_21_2.0"] and \
                     df.iloc[df_len-1]["close"] > df.iloc[df_len-2]["close"] and \
                         df.iloc[df_len-2]["EMA_8"] < df.iloc[df_len-2]["BBM_21_2.0"]

    # turn to sell จุดล่าง(แค่ไส้ทะลุ) => แท่งก่อนหน้าเป็นเขียว เปิดสูงกว่า EMA_8 แท่งต่อมาเป็นแดง high สูงกว่า BBU ปิดต่ำกว่าตัวที่แล้ว EMA_8 > BBM
    turn2sell50 = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["open"] > df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
                df.iloc[df_len-1]["high"] > df.iloc[df_len-1]["BBU_21_2.0"] and \
                    df.iloc[df_len-1]["close"] < df.iloc[df_len-2]["close"] and \
                         df.iloc[df_len-2]["EMA_8"] > df.iloc[df_len-2]["BBM_21_2.0"]

    # ระวังกลับตัว Sell => แท่งก่อนหน้าเขียว high ชน EMA_8 แท่งต่อมาแดง
    beware_sell_ema = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["high"] > df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"]

    # ระวังกลับตัว Sell => แท่งก่อนหน้าเขียว high ชน BBM แท่งต่อมาแดง
    beware_sell_bbm = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["high"] > df.iloc[df_len-2]["BBU_21_2.0"] and \
            df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"]

    # ระวังกลับตัว Buy => แท่งก่อนหน้าแดง low ชน EMA_8 แท่งต่อมาเขียว
    beware_buy_ema = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["low"] < df.iloc[df_len-2]["EMA_8"] and \
            df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"]

    # ระวังกลับตัว Buy => แท่งก่อนหน้าแดง low ชน BBM แท่งต่อมาเขียว
    beware_buy_bbm = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-2]["low"] < df.iloc[df_len-2]["BBU_21_2.0"] and \
            df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"]

    # ระวังกลับตัว Sell => แท่งก่อนหน้าเขียว แท่งต่อมาแดง high ชน EMA_8 
    beware_sell_ema2 = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["high"] > df.iloc[df_len-1]["EMA_8"] 

    # ระวังกลับตัว Buy => แท่งก่อนหน้าแดง แท่งต่อมาเขียว low ชน EMA_8 
    beware_buy_ema2 = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["low"] < df.iloc[df_len-1]["EMA_8"]

    # ระวังกลับตัว Sell => แท่งก่อนหน้าเขียว แท่งต่อมาแดง high ชน BBM 
    beware_sell_bbm2 = df.iloc[df_len-2]["close"] > df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] < df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["high"] > df.iloc[df_len-1]["BBU_21_2.0"] 
    
    # ระวังกลับตัว Buy => แท่งก่อนหน้าแดง แท่งต่อมาเขียว low ชน BBM 
    beware_buy_bbm2 = df.iloc[df_len-2]["close"] < df.iloc[df_len-2]["open"] and \
        df.iloc[df_len-1]["close"] > df.iloc[df_len-1]["open"] and \
            df.iloc[df_len-1]["low"] < df.iloc[df_len-1]["BBU_21_2.0"]
            

    if cnd_follow_buy1 or cnd_follow_buy2 or cnd_follow_buy3:
        signal_test= 'Follow Buy'
    elif cnd_follow_sell1 or cnd_follow_sell2 or cnd_follow_sell3 :
        signal_test= 'Follow Sell'
    elif turn2buy100 :
        signal_test= 'Buy 100'
    elif turn2sell100 :
        signal_test= 'Sell 100'
    elif turn2buy50 :
        signal_test= 'Buy 50'
    elif turn2sell50 :
        signal_test= 'Sell 50'
    elif ch2buy :
        signal_test= 'Change to Buy'
    elif ch2sell :
        signal_test= 'Change to Sell'
    elif beware_sell_ema :
        signal_test= 'Beware change to Sell [EMA_8]'
    elif beware_sell_ema2:
        signal_test= 'Beware2 change to Sell [EMA_8]'
    elif beware_sell_bbm :
        signal_test= 'Beware change to Sell [BBM]'
    elif  beware_sell_bbm2:
        signal_test= 'Beware2 change to Sell [BBM]'
    elif beware_buy_ema :
        signal_test= 'Beware change to Buy [EMA_8]'
    elif beware_buy_ema2:
        signal_test= 'Beware2 change to Buy [EMA_8]'
    elif beware_buy_bbm :
        signal_test= 'Beware change to Buy [BBM]'
    elif beware_buy_bbm2:
        signal_test= 'Beware2 change to Buy [BBM]'

    return signal_test