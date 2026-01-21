import csv
import random

# 定义中文姓名列表
first_names = ["张", "王", "李", "赵", "陈", "刘", "杨", "黄", "吴", "周"]
last_names = ["伟", "芳", "娜", "敏", "静", "秀英", "丽", "强", "磊", "洋"]

# 生成100个中文姓名
students = [random.choice(first_names) + random.choice(last_names) for _ in range(15)]

# 生成数据
data = []
for student in students:
    math_score = random.randint(50, 100)  # 数学成绩
    chinese_score = random.randint(50, 100)  # 语文成绩
    english_score = random.randint(50, 100)  # 英语成绩
    data.append([student, math_score, chinese_score, english_score])

# 写入CSV文件
with open("score.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["姓名", "数学成绩", "语文成绩", "英语成绩"])  # 写入表头
    writer.writerows(data)  # 写入数据

print("score.csv 文件已生成，包含 {} 条数据！".format(len(data)))