import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import user_setting

temp_date =''

# 目前總資金
all_assent = 0

# 股票資產
stock_assent = 0

# cash
cash_assent = 0

# 做圖數據
drawer_data = [] #[x,y]
drawer_data2 = [] #[x,y]

# 設置中文字體
plt.rcParams['font.family'] = 'SimSun'

# 擁有的張數
stock_shares_tw = []
stock_shares_us = []

# 定義回測的時間範圍（20年）
start_date = '2003-01-01'
end_date = '2023-01-01'

# 指定台幣兌美元的匯率資料，代碼為'USDTWD=X'
currency_pair = 'USDTWD=X'

# 創建一個空的DataFrame來存儲股票資料
stock_data_tw = pd.DataFrame()
stock_data_us = pd.DataFrame()

def data_to_csv():
    global stock_data_tw  # 聲明為全域變數
    # 使用yfinance獲取股票資料並存儲到DataFrame中
    for symbol in user_setting.stock_symbols_tw:
        data = yf.download(symbol, start=start_date, end=end_date)
        stock_data_tw[symbol] = data['Adj Close']

    # 將股票資料保存到CSV檔中
    stock_data_tw.to_csv('stock_data_tw.csv')

    global stock_data_us  # 聲明為全域變數
    for symbol in user_setting.stock_symbols_us:
        data = yf.download(symbol, start=start_date, end=end_date)
        stock_data_us[symbol] = data['Adj Close']

    # 將股票資料保存到CSV檔中
    stock_data_us.to_csv('stock_data_us.csv')

def data_from_csv():
    global stock_data_tw,stock_data_us  # 聲明為全域變數
    stock_data_tw = pd.read_csv('stock_data_tw.csv', index_col=0, parse_dates=True)
    stock_data_us = pd.read_csv('stock_data_us.csv', index_col=0, parse_dates=True)

def draw():
    global stock_data_tw,stock_data_us  # 聲明為全域變數
    # 繪製股價圖表
    plt.figure(figsize=(12, 6))

    for symbol in user_setting.stock_symbols_tw:
        plt.plot(stock_data_tw.index, stock_data_tw[symbol], label=symbol)
    for symbol in user_setting.stock_symbols_us:
        plt.plot(stock_data_us.index, stock_data_us[symbol], label=symbol)

    plt.title('股票價格表現')
    plt.xlabel('日期')
    plt.ylabel('股價')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
# 檢查指定日期是否在兩個CSV檔中同時存在

def date_exists_in_csv(date, csv_files):
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file, index_col=0, parse_dates=True)
            if date not in df.index:
                return False
        except Exception as e:
            return False
    return True

def year_count(current_date,days_to_add):

    csv_files = ['stock_data_tw.csv', 'stock_data_us.csv']

    # 將日期字串轉換為 datetime 物件
    date_obj = datetime.strptime(current_date, '%Y-%m-%d')
    new_date_obj = date_obj + timedelta(days=days_to_add) #365
    new_date = new_date_obj.strftime('%Y-%m-%d')

    while not date_exists_in_csv(new_date, csv_files):
        date_obj = datetime.strptime(new_date, '%Y-%m-%d')
        date_obj += timedelta(days=1)
        new_date = date_obj.strftime('%Y-%m-%d')
    
    print(f"鄰近的日期： {new_date} ")
    return new_date

def search(name, date):
    global stock_data_tw, stock_data_us  # 聲明為全域變數

    # 根據股票名稱選擇要查詢的資料框
    if name in user_setting.stock_symbols_tw:
        df = stock_data_tw
    elif name in user_setting.stock_symbols_us:
        df = stock_data_us
    else:
        print(f"股票 {name} 不存在於資料中")
        return
    
    # 使用while迴圈查找股價，如果找不到，則將日期往後延一天，直到找到為止
    while date not in df.index:
        # 將日期字串轉換為日期物件，以便進行日期操作
        current_date = pd.to_datetime(date)
        # 將日期加一天
        current_date += pd.DateOffset(days=1)
        # 將日期轉換回字串
        date = current_date.strftime('%Y-%m-%d')

    # 在找到股價後，將其取出並列印
    stock_price = df.loc[date, name]
    stock_price_rounded = round(stock_price, 1)
    print(f'{name}在{date}的股價為：{stock_price_rounded}')
    return stock_price_rounded

def exchange(date):
    # 讀取存儲的匯率資料
    exchange_rate_data = pd.read_csv('exchange_rate_usd_to_twd.csv', index_col=0, parse_dates=True)
    exchange_price = exchange_rate_data.loc[date]
    res = exchange_price["Close"].mean()
    result = round(res, 1)
    # print(f'匯率在{date}的當日平均為：{result}')
    return result
    
def download_exchange():
    # 使用yfinance獲取匯率資料
    exchange_rate = yf.download(currency_pair, start=start_date, end=end_date)

    # 將匯率資料保存到CSV檔
    exchange_rate.to_csv('exchange_rate_usd_to_twd.csv')

def num_shares(money,stock_name,date): #money是台幣
    # 計算可購買的股票數量
    stock_price = search(stock_name,date)
    number_of_shares = money // stock_price

    # print(f'您可以購買 {number_of_shares} 股 {stock_name} 股票。')
    return number_of_shares

# def end_calculate(date,):

def find_lower(percent,name,now_price):
    global stock_data_tw, stock_data_us  # 聲明為全域變數
    line_price = now_price*(1-percent*0.01)
    print(line_price)
    # 根據股票名稱選擇要查詢的資料框
    if name in user_setting.stock_symbols_tw:
        df = stock_data_tw
    elif name in user_setting.stock_symbols_us:
        df = stock_data_us
    else:
        print(f"股票 {name} 不存在於資料中")
        return

    # 選擇2018年的資料
    df_2018 = df['2018-01-02':'2018-12-31']

    # 找到2018年內股價低於指定閾值的日期和股價
    lower_prices_2018 = df_2018[df_2018[name] < line_price]

    # 列印找到的日期和股價
    if not lower_prices_2018.empty:
        print(f"{name} 在2018年內股價低於{percent}%的閾值的日期和股價：")
        print(lower_prices_2018[[name]])
    else:
        print(f"{name} 在2018年內沒有低於{percent}%的閾值的日期。")

#   把現有的股票全部換成現金 得到目前的總股票資產市值
def stock_exchange_money(date):
    global stock_data_tw, stock_data_us,all_assent,stock_shares_tw,stock_shares_us  # 聲明為全域變數
    market_value = 0
    # 計算每支股票的市值，並列印出來
    for i, position in enumerate(stock_shares_tw, start=0):
        stock_price = search(user_setting.stock_symbols_tw[i], date)
        market_value += round(position * stock_price,1)  # 計算市值
    for i, position in enumerate(stock_shares_us, start=0):
        stock_price = search(user_setting.stock_symbols_us[i], date) * exchange(date)
        market_value += round(position * stock_price,1)  # 計算市值
    print(f'股票總市值：{market_value}') 
    return   market_value     

def balance_per_year(date):
    global stock_data_tw, stock_data_us,all_assent,cash_assent,drawer_data,drawer_data2,assent_buffer,stock_assent,stock_shares_tw,stock_shares_us,temp_date  # 聲明為全域變數
    # 把全部股票換成現金再重新分配

    stock_assent = stock_exchange_money(date)
    all_assent = cash_assent + stock_assent + user_setting.put_in
    assent_buffer += user_setting.put_in
    print(temp_date,'目前總資產 ------> ',all_assent)
    print(temp_date,'已投入資金 ------> ',assent_buffer)

    for i in range(len(user_setting.percent_tw)):
        stock_name = user_setting.stock_symbols_tw[i]
        result = round(all_assent * user_setting.percent_tw[i] * search(stock_name,  temp_date),1)
        shares = num_shares(all_assent * user_setting.percent_tw[i],stock_name,temp_date)
        stock_shares_tw[i] = shares
        # print(f"投資 {stock_name} 的結果: {result}")
    for i in range(len(user_setting.percent_us)):
        stock_name = user_setting.stock_symbols_us[i]
        result = round(all_assent * user_setting.percent_us[i] * search(stock_name, temp_date) ,1)
        shares = num_shares(all_assent * user_setting.percent_us[i]/exchange(temp_date),stock_name,temp_date)
        stock_shares_us[i] = shares

    stock_assent = stock_exchange_money(temp_date)
    cash_assent = all_assent - stock_assent
    print('現金水位目前',cash_assent)
    drawer_data.append([temp_date, round(all_assent,1)])  # 添加第一個資料點 [x=1, y=2]
    drawer_data2.append([temp_date, round(assent_buffer,1)])  # 添加第一個資料點 [x=1, y=2]


def drawer(drawer_data):
    # 示例數據
    # x = [1, 2, 3, 4, 5]  # x軸資料點
    # y = [10, 14, 8, 17, 6]  # y軸資料點
    # 提取x和y值
    x_values = [point[0] for point in drawer_data]
    y_values = [point[1] for point in drawer_data]
    y2_values = [point[1] for point in drawer_data2]

    # 創建散點圖
    plt.plot(x_values, y_values, label='資產總額', color='b', marker='o')
    plt.plot(x_values, y2_values, label='投入總金額', color='r', marker='o')

    # 添加座標標籤
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        plt.annotate(f'({x}, {y})', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    # 添加標題和標籤
    plt.title('回測資產分佈')
    plt.xlabel('X軸(年份)')
    plt.ylabel('Y軸(資產額)')

    # 顯示圖表
    plt.legend()
    plt.grid(True)
    plt.show()

def check_portfolio_availability(start_date, investment_years, portfolio):
    # 讀取台股和美股的股價數據
    stock_data_tw = pd.read_csv('stock_data_tw.csv', index_col=0, parse_dates=True)
    stock_data_us = pd.read_csv('stock_data_us.csv', index_col=0, parse_dates=True)

    # 確定投資結束的日期
    start_date = pd.to_datetime(start_date)
    end_date = start_date + pd.DateOffset(years=investment_years)
    error_cnt = 0
    # 遍歷投資組合中的股票，檢查每個股票在投資期間是否都有資料
    for stock_symbol in portfolio:
        if stock_symbol in stock_data_tw.columns:
            df = stock_data_tw
        elif stock_symbol in stock_data_us.columns:
            df = stock_data_us
        else:
            print(f"股票 {stock_symbol} 不存在於資料中 可能未下載至csv")
            return False

        stock_data = df[start_date:end_date]

        if stock_data.isna().values.any():
            error_cnt += 1
            print(f"股票 {stock_symbol} 在投資期間存在 NaN 值")

    if(error_cnt > 0):
        return False
    return True

def profolio_execute():
    global stock_data_tw, stock_data_us,all_assent,cash_assent,assent_buffer,stock_assent,stock_shares_tw,stock_shares_us,temp_date  # 聲明為全域變數

    # 第一年投入計算
    for i in range(len(user_setting.percent_tw)):
        stock_name = user_setting.stock_symbols_tw[i]
        result = round(user_setting.first_put_in * user_setting.percent_tw[i] * search(stock_name, user_setting.first_date),1)
        shares = num_shares(user_setting.first_put_in * user_setting.percent_tw[i],stock_name,user_setting.first_date)
        stock_shares_tw.append(shares)  # 第一支股票有100股

        # print(f"投資 {stock_name} 的結果: {result}")

    for i in range(len(user_setting.percent_us)):
        stock_name = user_setting.stock_symbols_us[i]
        result = round(user_setting.first_put_in * user_setting.percent_us[i] * search(stock_name, user_setting.first_date) ,1)
        shares = num_shares(user_setting.first_put_in * user_setting.percent_us[i]/exchange(user_setting.first_date),stock_name,user_setting.first_date)
        stock_shares_us.append(shares)  # 第一支股票有100股

        # print(f"投資 {stock_name} 的結果: {result}")
    
    all_assent = user_setting.first_put_in
    stock_assent = stock_exchange_money(user_setting.first_date)
    cash_assent = all_assent - stock_assent
    print('現金水位目前',cash_assent)
    assent_buffer = all_assent
    print(user_setting.first_date,'目前總資產 ------> ',all_assent)
    print(user_setting.first_date,'已投入資金 ------> ',assent_buffer)
    drawer_data.append([user_setting.first_date, all_assent])  # 添加第一個資料點 [x=1, y=2]
    drawer_data2.append([user_setting.first_date, assent_buffer])  # 添加第一個資料點 [x=1, y=2]

    # 列印目前每支股票的張數
    for i, position in enumerate(stock_shares_tw, start=1):
        print(f'股票{i} 股數：{position}')
    for i, position in enumerate(stock_shares_us, start=1):
        print(f'股票{i} 股數：{position}') 

    print('*****************************')
    if(user_setting.balance == True):
        print('balance')
        temp_date = year_count(user_setting.first_date,365)
        balance_per_year(temp_date)
    else:
        print('no balance')
        # 還沒寫..
    
    # 列印目前每支股票的張數
    for i, position in enumerate(stock_shares_tw, start=1):
        print(f'股票{i} 股數：{position}')
    for i, position in enumerate(stock_shares_us, start=1):
        print(f'股票{i} 股數：{position}') 

    print('*****************************')
    for i in range(1, user_setting.investment_duration-2):
        if(user_setting.balance == True):
            print('balance')
            temp_date = year_count(temp_date,365)
            balance_per_year(temp_date)
        else:
            print('no balance')
            # 還沒寫..
    # find_lower(10,'2330.TW',196.9)
    # year_count(first_date,365)
    
    # 之後每一年計算

    drawer(drawer_data)
def main():
    data_to_csv()
    data_from_csv()
    # draw()
    # search('AAPL','2018-03-16')
    # exchange('2018-03-16')
    result_us = check_portfolio_availability(user_setting.first_date, user_setting.investment_duration, user_setting.stock_symbols_us)
    result_tw = check_portfolio_availability(user_setting.first_date, user_setting.investment_duration, user_setting.stock_symbols_tw)

    if result_us and result_tw:
        print("投資組合可行")
    else:
        print("投資組合存在問題")
        return

    profolio_execute()
    
if __name__ == "__main__":
    main()


