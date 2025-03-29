#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2025 ICodeWR（微信公众号同名）

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Module/Script Name: sklearnTest.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day09 exexample Script.

# uv add scikit-learn

import streamlit as st
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import matplotlib.pyplot as plt


# 加载数据
iris = load_iris()
X = iris.data
y = iris.target

# 训练模型
model = RandomForestClassifier()
model.fit(X, y)

# 创建应用
st.title('鸢尾花分类器')

# 侧边栏输入
st.sidebar.header('输入参数')
sepal_length = st.sidebar.slider('花萼长度', float(X[:, 0].min()), float(X[:, 0].max()), float(X[:, 0].mean()))
sepal_width = st.sidebar.slider('花萼宽度', float(X[:, 1].min()), float(X[:, 1].max()), float(X[:, 1].mean()))
petal_length = st.sidebar.slider('花瓣长度', float(X[:, 2].min()), float(X[:, 2].max()), float(X[:, 2].mean()))
petal_width = st.sidebar.slider('花瓣宽度', float(X[:, 3].min()), float(X[:, 3].max()), float(X[:, 3].mean()))

# 预测
input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
prediction = model.predict(input_data)
prediction_proba = model.predict_proba(input_data)

# 显示结果
st.subheader('预测结果')
st.write(f'预测种类: {iris.target_names[prediction[0]]}')
st.write('预测概率:')
proba_df = pd.DataFrame({
    '种类': iris.target_names,
    '概率': prediction_proba[0]
})
st.bar_chart(proba_df.set_index('种类'))

# 显示原始数据
if st.checkbox('显示原始数据'):
    st.subheader('鸢尾花数据集')
    df = pd.DataFrame(X, columns=iris.feature_names)
    df['种类'] = y
    st.write(df)