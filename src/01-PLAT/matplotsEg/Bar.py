import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

labels = ['苹果', '香蕉', '橙子']
values = [25, 40, 30]

fig, ax = plt.subplots()
ax.bar(labels, values, color=['red', 'yellow', 'orange'])
ax.set_ylabel('销量')
plt.show()

