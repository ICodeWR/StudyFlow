# image.py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 读取图像
img = mpimg.imread('image.jpg')

# 显示图像
plt.imshow(img)
plt.axis('off')
plt.title('Image Display')
plt.show()