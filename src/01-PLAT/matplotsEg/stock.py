import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 读取 CSV 文件
dates = []
open_prices = []
high_prices = []
low_prices = []
close_prices = []
volumes = []

with open('stock_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过表头
    for row in reader:
        dates.append(datetime.strptime(row[0], '%Y-%m-%d'))  # 日期
        open_prices.append(float(row[1]))  # 开盘价
        high_prices.append(float(row[2]))  # 最高价
        low_prices.append(float(row[3]))  # 最低价
        close_prices.append(float(row[4]))  # 收盘价
        volumes.append(int(row[5]))  # 成交量

# 2. 创建画布和子图
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# 3. 绘制股票价格走势图
ax1.plot(dates, open_prices, label='开盘价', marker='o', linestyle='-', color='blue')
ax1.plot(dates, high_prices, label='最高价', marker='^', linestyle='--', color='green')
ax1.plot(dates, low_prices, label='最低价', marker='v', linestyle='--', color='red')
ax1.plot(dates, close_prices, label='收盘价', marker='s', linestyle='-', color='purple')

ax1.set_title('股票价格走势图')
ax1.set_ylabel('价格')
ax1.legend()
ax1.grid(True)

# 4. 绘制成交量柱状图
ax2.bar(dates, volumes, color='orange', label='成交量')
ax2.set_title('成交量柱状图')
ax2.set_xlabel('日期')
ax2.set_ylabel('成交量')
ax2.legend()
ax2.grid(True)

# 5. 调整布局
plt.xticks(rotation=45)  # 旋转日期标签
plt.tight_layout()
plt.show()