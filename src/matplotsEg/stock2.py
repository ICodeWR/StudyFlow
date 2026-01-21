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

# 2. 股票价格走势图
def plot_stock_prices(dates, open_prices, high_prices, low_prices, close_prices):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, open_prices, label='开盘价', marker='o', linestyle='-', color='blue')
    plt.plot(dates, high_prices, label='最高价', marker='^', linestyle='--', color='green')
    plt.plot(dates, low_prices, label='最低价', marker='v', linestyle='--', color='red')
    plt.plot(dates, close_prices, label='收盘价', marker='s', linestyle='-', color='purple')
    
    plt.title('股票价格走势图')
    plt.xlabel('日期')
    plt.ylabel('价格')
    plt.xticks(rotation=45)  # 旋转日期标签
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 3. 成交量柱状图
def plot_volume(dates, volumes):
    plt.figure(figsize=(12, 6))
    plt.bar(dates, volumes, color='orange', label='成交量')
    
    plt.title('成交量柱状图')
    plt.xlabel('日期')
    plt.ylabel('成交量')
    plt.xticks(rotation=45)  # 旋转日期标签
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# 调用函数绘制图表
plot_stock_prices(dates, open_prices, high_prices, low_prices, close_prices)
plot_volume(dates, volumes)