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

# Module/Script Name: 06app.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day06 exexample Script.

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# 标题和简介
st.title("高级数据仪表盘")
st.write("支持动态交互、多图表联动与复杂布局")

# 数据加载
data_source = st.sidebar.radio("选择数据源", ["内置数据集", "上传 CSV"])
if data_source == "内置数据集":
    data = pd.DataFrame({
        "category": ["A", "B", "C", "D", "E"],
        "value": [28, 55, 43, 91, 20],
        "x": [1, 2, 3, 4, 5],
        "y": [5, 4, 3, 2, 1]
    })
else:
    uploaded_file = st.sidebar.file_uploader("上传 CSV", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)

if 'data' in locals():

    # 控制面板（侧边栏）
    st.sidebar.header("控制面板")
    x_axis = st.sidebar.selectbox("X 轴字段", data.columns)
    y_axis = st.sidebar.selectbox("Y 轴字段", data.columns)

    # 主界面布局
    tab1, tab2, tab3 = st.tabs(["Altair", "Plotly", "Vega-Lite"])

    with tab1:
        # Altair 图表
        st.subheader("Altair 交互式图表")
        chart = alt.Chart(data).mark_circle(size=100).encode(
            x=x_axis,
            y=y_axis,
            tooltip=list(data.columns)
        ).interactive()
        st.altair_chart(chart, use_container_width=True)

    with tab2:
        # Plotly 图表
        st.subheader("Plotly 3D 散点图")
        fig = px.scatter_3d(data, x=x_axis, y=y_axis, z="value", color="category")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Vega-Lite 图表
        st.subheader("Vega-Lite 柱状图")
        spec = {
            "mark": "bar",
            "encoding": {
                "x": {"field": x_axis, "type": "nominal"},
                "y": {"field": y_axis, "type": "quantitative"}
            }
        }
        st.vega_lite_chart(data, spec, use_container_width=True)

    # 数据详情扩展器
    with st.expander("查看原始数据"):
        st.dataframe(data.style.highlight_max(axis=0))

    # 统计信息列布局
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总行数", len(data))
    with col2:
        st.metric("最大值", data[y_axis].max())
    with col3:
        st.metric("最小值", data[y_axis].min())

else:
    st.warning("请先选择数据源")
