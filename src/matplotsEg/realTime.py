# realTime.py
import matplotlib.pyplot as plt
import numpy as np
import time

# 初始化数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 动态更新折线图
plt.ion()
fig, ax = plt.subplots()
line, = ax.plot(x, y)

for i in range(100):
    y = np.sin(x + i / 10)
    line.set_ydata(y)
    plt.draw()
    plt.pause(0.1)

plt.ioff()
plt.show()