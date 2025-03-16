import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取 CSV 文件
data = np.genfromtxt('score.csv', delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
names = data[:, 0]  # 姓名
math_scores = data[:, 1].astype(float)  # 数学成绩
chinese_scores = data[:, 2].astype(float)  # 语文成绩
english_scores = data[:, 3].astype(float)  # 英语成绩

# 2. 成绩分布饼图
def plot_score_distribution(math_scores, chinese_scores, english_scores):
    # 定义成绩等级
    bins = [0, 60, 75, 90, 100]
    labels = ['不及格', '及格', '良好', '优秀']
    
    # 计算每个等级的比例
    def get_distribution(scores):
        hist, _ = np.histogram(scores, bins=bins)
        return hist / len(scores)
    
    math_dist = get_distribution(math_scores)
    chinese_dist = get_distribution(chinese_scores)
    english_dist = get_distribution(english_scores)
    
    # 绘制饼图
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].pie(math_dist, labels=labels, autopct='%1.1f%%', startangle=90)
    axes[0].set_title('数学成绩分布')
    axes[1].pie(chinese_dist, labels=labels, autopct='%1.1f%%', startangle=90)
    axes[1].set_title('语文成绩分布')
    axes[2].pie(english_dist, labels=labels, autopct='%1.1f%%', startangle=90)
    axes[2].set_title('英语成绩分布')
    plt.show()

# 3. 科目平均分柱状图
def plot_average_scores(math_scores, chinese_scores, english_scores):
    # 计算各科平均分
    avg_scores = [np.mean(math_scores), np.mean(chinese_scores), np.mean(english_scores)]
    subjects = ['数学', '语文', '英语']
    
    # 绘制柱状图
    plt.figure(figsize=(8, 5))
    plt.bar(subjects, avg_scores, color=['skyblue', 'lightgreen', 'salmon'])
    plt.title('各科平均分')
    plt.xlabel('科目')
    plt.ylabel('平均分')
    plt.show()

# 4. 不及格率折线图
def plot_fail_rate(math_scores, chinese_scores, english_scores):
    # 计算不及格率
    fail_rate = [
        np.sum(math_scores < 60) / len(math_scores) * 100,
        np.sum(chinese_scores < 60) / len(chinese_scores) * 100,
        np.sum(english_scores < 60) / len(english_scores) * 100
    ]
    subjects = ['数学', '语文', '英语']
    
    # 绘制折线图
    plt.figure(figsize=(8, 5))
    plt.plot(subjects, fail_rate, marker='o', color='red')
    plt.title('各科不及格率')
    plt.xlabel('科目')
    plt.ylabel('不及格率 (%)')
    plt.grid(True)
    plt.show()

# 5. 总成绩折线图
def plot_total_scores(names, math_scores, chinese_scores, english_scores):
    # 计算每个学生的总成绩
    total_scores = math_scores + chinese_scores + english_scores
    
    # 绘制折线图
    plt.figure(figsize=(10, 5))
    plt.plot(names, total_scores, marker='o', color='blue')
    plt.title('学生总成绩')
    plt.xlabel('学生姓名')
    plt.ylabel('总成绩')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

# 调用函数绘制图表
plot_score_distribution(math_scores, chinese_scores, english_scores)
plot_average_scores(math_scores, chinese_scores, english_scores)
plot_fail_rate(math_scores, chinese_scores, english_scores)
plot_total_scores(names, math_scores, chinese_scores, english_scores)