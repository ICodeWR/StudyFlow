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

# Module/Script Name: app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day02 exexample Script.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 设置 matplotlib 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 标题和简介
st.title("数据仪表盘示例")
st.write("这是一个简单的数据仪表盘，展示了 Streamlit 的核心组件和布局方式。")

# 侧边栏
st.sidebar.title("设置")
chart_type = st.sidebar.selectbox("选择图表类型", ["折线图", "柱状图"])

# 创建示例数据
data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

# 列布局
col1, col2 = st.columns([1, 2])

with col1:
    st.write("### 交互式 DataFrame")
    st.dataframe(data)

with col2:
    st.write("### 图表")
    if chart_type == "折线图":
        st.line_chart(data)
    else:
        st.bar_chart(data)

# 选项卡
tab1, tab2 = st.tabs(["Matplotlib 图表", "关于"])

with tab1:
    st.write("### Matplotlib 示例")
    fig, ax = plt.subplots()
    ax.plot(data["A"], label="A")
    ax.plot(data["B"], label="B")
    ax.set_title("Matplotlib 图表")
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.write("### 关于")
    st.write("这是一个 Streamlit 数据仪表盘示例。")
