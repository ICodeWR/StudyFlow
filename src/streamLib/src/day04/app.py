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
# Description: streamlit day04 exexample Script.

import streamlit as st
import pandas as pd

# 标题和简介
st.title("数据探索工具")
st.write("上传 CSV 文件并探索数据。")

# 文件上传
uploaded_file = st.file_uploader("上传 CSV 文件", type=["csv"])

if uploaded_file is not None:
    # 读取 CSV 文件
    data = pd.read_csv(uploaded_file)
    st.write("### 原始数据")
    st.dataframe(data)

    # 基本数据分析
    st.write("### 基本数据分析")
    st.write(f"**行数:** {len(data)}")
    st.write(f"**列数:** {len(data.columns)}")
    st.write("**列名:**")
    st.write(data.columns.tolist())

    # 数据过滤
    st.write("### 数据过滤")
    columns = data.columns.tolist()
    selected_columns = st.multiselect("选择要显示的列", columns, default=columns)
    if selected_columns:
        filtered_data = data[selected_columns]
        st.write("### 过滤后的数据")
        st.dataframe(filtered_data)

    # 数据统计
    st.write("### 数据统计")
    if st.checkbox("显示数据统计信息"):
        st.write(data.describe())

    # 数据下载
    st.write("### 数据下载")
    if st.button("下载过滤后的数据为 CSV"):
        csv = filtered_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="下载 CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )
else:
    st.write("请上传 CSV 文件以开始探索数据。")

