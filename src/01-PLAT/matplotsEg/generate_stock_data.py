import csv
import random
from datetime import datetime, timedelta

# 生成随机股票数据
def generate_stock_data(start_date, num_days):
    data = []
    current_date = start_date
    for _ in range(num_days):
        # 生成随机价格
        open_price = round(random.uniform(100, 200), 2)  # 开盘价
        high_price = round(open_price * random.uniform(1.0, 1.1), 2)  # 最高价
        low_price = round(open_price * random.uniform(0.9, 1.0), 2)  # 最低价
        close_price = round(random.uniform(low_price, high_price), 2)  # 收盘价
        volume = random.randint(100000, 500000)  # 成交量
        
        # 添加到数据列表
        data.append([current_date.strftime('%Y-%m-%d'), open_price, high_price, low_price, close_price, volume])
        
        # 增加一天
        current_date += timedelta(days=1)
    return data

# 定义起始日期和天数
start_date = datetime(2023, 1, 1)
num_days = 100  # 生成100天的数据

# 生成数据
stock_data = generate_stock_data(start_date, num_days)

# 写入CSV文件
with open('stock_data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['日期', '开盘价', '最高价', '最低价', '收盘价', '成交量'])  # 写入表头
    writer.writerows(stock_data)  # 写入数据

print("stock_data.csv 文件已生成，包含 {} 条数据！".format(len(stock_data)))