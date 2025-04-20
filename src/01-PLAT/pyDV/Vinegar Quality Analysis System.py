# -*- coding: utf-8 -*-

"""
老陈醋生产质量分析系统
功能包含：
1. 生产数据可视化分析
2. 质量指标相关性分析
3. 质量预测模型
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 1. 模拟生成生产数据
def generate_production_data(num_samples=100):
    """
    生成模拟老陈醋生产数据
    包含以下特征：
    - 生产批次
    - 发酵温度(℃)
    - 发酵时间(天)
    - pH值
    - 总酸(g/100ml)
    - 不挥发酸(g/100ml)
    - 还原糖(g/100ml)
    - 氨基酸态氮(g/100ml)
    - 菌落总数(CFU/ml)
    - 大肠菌群(MPN/100ml)
    - 感官评分(0-100)
    """
    np.random.seed(42)
    
    data = {
        '批次号': [f'PC{2024000+i}' for i in range(num_samples)],
        '发酵温度': np.random.normal(32, 2, num_samples),
        '发酵时间': np.random.randint(15, 45, num_samples),
        'pH值': np.random.uniform(3.2, 3.8, num_samples),
        '总酸': np.random.normal(6.5, 0.5, num_samples),
        '不挥发酸': np.random.normal(3.8, 0.3, num_samples),
        '还原糖': np.random.normal(2.5, 0.4, num_samples),
        '氨基酸态氮': np.random.normal(0.4, 0.05, num_samples),
        '菌落总数': np.random.lognormal(3, 0.5, num_samples),
        '大肠菌群': np.random.poisson(3, num_samples),
        '感官评分': np.random.normal(85, 5, num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # 添加10%的缺失值
    mask = np.random.rand(*df.shape) < 0.1
    df = df.mask(mask)
    
    return df

# 2. 数据预处理
def preprocess_data(df):
    # 填充缺失值
    numerical_cols = df.select_dtypes(include=np.number).columns.tolist()
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # 处理异常值
    df['发酵温度'] = np.clip(df['发酵温度'], 25, 38)
    df['pH值'] = np.clip(df['pH值'], 3.0, 4.0)
    
    # 添加质量等级分类
    conditions = [
        (df['感官评分'] >= 90),
        (df['感官评分'] >= 80) & (df['感官评分'] < 90),
        (df['感官评分'] < 80)
    ]
    choices = ['特级', '一级', '二级']
    # df['质量等级'] = np.select(conditions, choices)
    df['质量等级'] = np.select(conditions, choices, default='二级')  # 添加默认值

    
    return df

# 3. 数据可视化分析
def visualize_data(df):
    plt.figure(figsize=(15, 10))
    
    # 关键指标分布
    plt.subplot(2, 2, 1)
    sns.histplot(df['总酸'], kde=True)
    plt.title('总酸含量分布')
    
    plt.subplot(2, 2, 2)
    sns.scatterplot(x='发酵时间', y='总酸', hue='质量等级', data=df)
    plt.title('发酵时间与总酸关系')
    
    plt.subplot(2, 2, 3)
    sns.boxplot(x='质量等级', y='感官评分', data=df)
    plt.title('质量等级评分分布')
    
    plt.subplot(2, 2, 4)
    corr_matrix = df.corr(numeric_only=True)
    sns.heatmap(corr_matrix[['感官评分']], annot=True, cmap='coolwarm')
    plt.title('指标与感官评分相关性')
    
    plt.tight_layout()
    plt.show()

# 4. 质量预测模型
def build_quality_model(df):
    # 特征选择
    features = ['发酵温度', '发酵时间', 'pH值', '总酸', 
               '不挥发酸', '还原糖', '氨基酸态氮']
    target = '感官评分'
    
    X = df[features]
    y = df[target]
    
    # 数据分割
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    
    # 模型训练
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 模型评估
    y_pred = model.predict(X_test)
    print(f'模型性能:')
    print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}')
    print(f'R²: {r2_score(y_test, y_pred):.2f}')
    
    # 特征重要性
    importance = pd.Series(model.feature_importances_, index=features)
    importance.sort_values(ascending=False, inplace=True)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=importance.values, y=importance.index)
    plt.title('特征重要性分析')
    plt.show()
    
    return model, features

# 主程序
if __name__ == "__main__":
    # 生成并加载数据
    production_data = generate_production_data(200)
    
    # 数据预处理
    clean_data = preprocess_data(production_data)
    
    # 数据分析
    print("数据统计摘要:")
    print(clean_data.describe())
    
    print("\n质量等级分布:")
    print(clean_data['质量等级'].value_counts())
    
    # 数据可视化
    visualize_data(clean_data)
    
    # 构建预测模型
    quality_model, features = build_quality_model(clean_data)
    
    # 示例预测
    sample_data = pd.DataFrame([[
        33.5, 28, 3.5, 6.8, 
        3.9, 2.6, 0.42
    ]], columns=features)
    
    predicted_score = quality_model.predict(sample_data)
    print(f"\n预测感官评分: {predicted_score[0]:.1f}")

# 5. 生产建议生成
def generate_recommendations(df):
    recommendations = []
    
    # 基于温度分析
    optimal_temp = df.groupby('质量等级')['发酵温度'].mean()['特级']
    recommendations.append(
        f"建议保持发酵温度在{optimal_temp:.1f}℃左右")
    
    # 基于时间分析
    best_time = df.groupby('质量等级')['发酵时间'].median()['特级']
    recommendations.append(
        f"建议发酵时间控制在{best_time}天左右")
    
    # 基于pH分析
    best_ph = df[df['质量等级'] == '特级']['pH值'].median()
    recommendations.append(
        f"建议控制pH值在{best_ph:.2f}范围内")
    
    print("\n生产优化建议:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

# 运行建议生成
generate_recommendations(clean_data)