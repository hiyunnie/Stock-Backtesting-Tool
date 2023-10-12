# 第一筆
first_put_in = 600 * 10000 #w

# 每年初再平衡
balance = True

# 定期投入
put_in = 50 * 10000 #w

# 投入時間點
first_date = '2008-09-25'
investment_duration = 14

# 如果該股跌幅超過15%會加碼
down_line = 15 #%
more_put_in = 5*10000 #w

# 定義要追蹤的台股和美股的股票代碼
stock_symbols_tw = ['0050.TW']#, '00631L.TW']
percent_tw       = [0.30     ]#,0.15        ]

stock_symbols_us = ['VXUS', 'SPY', 'VT']
percent_us       = [0.30,0.30,  0.10   ]