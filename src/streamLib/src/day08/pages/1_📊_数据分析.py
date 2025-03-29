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

# Module/Script Name: 1_📊_数据分析.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day08 exexample Script.

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 数据分析中心")

# 上传数据
with st.expander("数据上传", expanded=True):
    uploaded_file = st.file_uploader("选择CSV文件", type=["csv"])
    
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    
    # 双列布局
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("数据预览")
        st.dataframe(data.head(10))
        
    with col2:
        st.subheader("可视化分析")
        chart_type = st.selectbox("图表类型", ["散点图", "柱状图", "折线图"])
        x_axis = st.selectbox("X轴字段", data.columns)
        y_axis = st.selectbox("Y轴字段", data.columns)
        
        if chart_type == "散点图":
            fig = px.scatter(data, x=x_axis, y=y_axis)
        elif chart_type == "柱状图":
            fig = px.bar(data, x=x_axis, y=y_axis)
        else:
            fig = px.line(data, x=x_axis, y=y_axis)
            
        st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("请先上传数据文件")
