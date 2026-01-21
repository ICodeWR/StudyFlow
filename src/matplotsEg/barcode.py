# barcode.py
import matplotlib.pyplot as plt
import numpy as np

# 生成条形码数据
code = np.array([1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1])

# 绘制条形码
plt.imshow(code.reshape(1, -1), cmap='binary', aspect='auto')
plt.axis('off')
plt.title('Barcode')
plt.show()