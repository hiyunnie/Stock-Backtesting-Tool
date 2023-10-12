import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

draw_plot = False
# 獲取 0050 的歷史價格資料
stock_symbol = '0050.TW'
start_date = '2003-01-01'
end_date = '2023-01-01'
data = yf.download(stock_symbol, start=start_date, end=end_date)

# 計算每日收益率
data['Daily_Return'] = data['Adj Close'].pct_change()

# 計算年度收益率
annual_returns = data['Daily_Return'].groupby(data.index.year).agg(lambda x: (x + 1).prod() - 1)

# 列印 20 年的年度收益率
print("0050過去 20 年的年度收益率：")
print(annual_returns)
print(annual_returns.mean())
# 計算 20 年的標準差和 Sharpe 比率
long_term_std_dev = data['Daily_Return'].std()
risk_free_rate = 0.01  # 假設無風險利率為 1%
long_term_sharpe_ratio = (annual_returns.mean() - risk_free_rate) / long_term_std_dev

# 列印長期標準差和 Sharpe 比率
print("\n20 年的長期標準差：")
print(long_term_std_dev)
print("\n20 年的長期 Sharpe 比率：")
print(long_term_sharpe_ratio)


