import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 1. 准备数据
x = np.linspace(0, 2*np.pi, 100)  # 生成0到2π的100个点
y = np.sin(x)                     # 计算每个点的正弦值

# 2. 创建画布和坐标轴
fig, ax = plt.subplots()

# 3. 绘制折线图
ax.plot(x, y, label='sin(x)', color='blue', linestyle='--')

# 4. 添加标签和标题
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.set_title('正弦函数曲线')
ax.legend()  # 显示图例

# 5. 显示图表
plt.show()

