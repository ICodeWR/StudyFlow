# interactive.py
import matplotlib.pyplot as plt
import numpy as np

# 生成数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 交互式绘图
plt.plot(x, y, label='sin(x)', color='blue')
plt.title('Interactive Plot')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()