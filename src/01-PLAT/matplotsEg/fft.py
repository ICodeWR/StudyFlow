# fft.py
import matplotlib.pyplot as plt
import numpy as np

# 生成信号数据
t = np.linspace(0, 1, 500)
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)

# 计算傅里叶变换
fourier_transform = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(t), t[1] - t[0])

# 绘制信号和傅里叶变换结果
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, signal, label='Signal', color='blue')
plt.title('Signal in Time Domain')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(frequencies, np.abs(fourier_transform), label='Fourier Transform', color='red')
plt.title('Fourier Transform')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.legend()

plt.tight_layout()
plt.show()