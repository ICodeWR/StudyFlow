import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = 100 * np.random.rand(50)

fig, ax = plt.subplots()
ax.scatter(x, y, c=colors, s=sizes, alpha=0.5)
ax.set_title('随机散点图')
plt.show()

