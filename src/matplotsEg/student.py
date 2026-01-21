# student.py
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 从 CSV 文件读取数据
# scores = np.loadtxt('score.csv', delimiter=',', skiprows=1, encoding='utf-8', usecols=2)
scores = np.genfromtxt('score.csv', delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
score_names = ('数学', '语文', '英语')
student_number = 40

# 绘制成绩区间统计饼图
def plot_pie(ax, name, scores):
    labels = ['<60', '60-69', '70-79', '80-89', '90-100']
    count = [np.sum(scores < 60),
             np.sum((scores >= 60) & (scores < 70)),
             np.sum((scores >= 70) & (scores < 80)),
             np.sum((scores >= 80) & (scores < 90)),
             np.sum(scores >= 90)]
    ax.pie(count, labels=labels, autopct='%1.1f%%')
    ax.set_title(f'{name}成绩区间统计')

# 绘制科目平均分柱状图
def plot_bar(ax, score_names, score_average):
    ax.bar(score_names, score_average, color=['red', 'green', 'blue'])
    ax.set_title('各科平均成绩对比')
    ax.set_ylabel('平均成绩')

# 绘制不及格率折线图
def plot_fail_rate(ax, fail_rates, score_names):
    ax.plot(score_names, fail_rates, marker='o')
    ax.set_title('各科不及格率')
    ax.set_ylabel('不及格率')

# 绘制总成绩折线图
def plot_total_score(ax, student_ids, total_scores):
    ax.plot(student_ids, total_scores, marker='o')
    ax.set_title('学生总成绩')
    ax.set_xlabel('姓名')
    ax.set_ylabel('总成绩')

# 主函数
def main():
    fig, ((ax0, ax1, ax2), (ax3, ax4, ax5)) = plt.subplots(2, 3, figsize=(12, 8))
    score_average = np.mean(scores[:, 1:].astype(float), axis=0)
    print(score_average)

    fail_rates = [np.sum(scores[:, i].astype(float) < 60) / student_number for i in range(1, 4)]
    total_scores = np.sum(scores[:, 1:].astype(float), axis=1)
    student_ids = scores[:, 0]

    plot_pie(ax0, score_names[0], scores[:, 1].astype(float))
    plot_pie(ax1, score_names[1], scores[:, 2].astype(float))
    plot_pie(ax2, score_names[2], scores[:, 3].astype(float))
    plot_bar(ax3, score_names, score_average)
    plot_fail_rate(ax4, fail_rates, score_names)
    plot_total_score(ax5, student_ids, total_scores)

    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()

