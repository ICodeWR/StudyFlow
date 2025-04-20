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

# Module/Script Name: 2_🗃️_数据管理.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
import pandas as pd
from utils.database import query_db, get_connection

st.title("🗃️ 数据管理")

# 标签输入组件
from components.tag_input import tag_input

# 数据表选择
tables = query_db("SELECT name FROM sqlite_master WHERE type='table'")
selected_table = st.selectbox("选择数据表", tables['name'].tolist())

# 显示表数据
if selected_table:
    df = query_db(f"SELECT * FROM {selected_table} LIMIT 1000")
    st.dataframe(df, use_container_width=True)
    
    # 数据操作选项卡
    tab1, tab2, tab3 = st.tabs(["查询", "编辑", "导入"])
    
    with tab1:
        st.subheader("自定义查询")
        query = st.text_area("输入SQL查询语句", f"SELECT * FROM {selected_table} LIMIT 100")
        if st.button("执行查询"):
            try:
                result = query_db(query)
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"查询错误: {str(e)}")
    
    with tab2:
        if st.session_state.auth["role"] not in ["admin", "editor"]:
            st.warning("您没有编辑权限")
        else:
            st.subheader("数据编辑")
            selected_columns = st.multiselect("选择显示的列", df.columns.tolist(), default=df.columns.tolist())
            edited_df = st.data_editor(df[selected_columns], use_container_width=True)
            
            if st.button("保存更改"):
                conn = get_connection()
                try:
                    edited_df.to_sql(selected_table, conn, if_exists="replace", index=False)
                    st.success("数据保存成功!")
                except Exception as e:
                    st.error(f"保存失败: {str(e)}")
    
    with tab3:
        st.subheader("数据导入")
        upload_file = st.file_uploader("上传CSV文件", type=["csv"])
        if upload_file:
            new_data = pd.read_csv(upload_file)
            st.write("预览数据:")
            st.dataframe(new_data.head())
            
            if st.button("导入数据"):
                conn = get_connection()
                try:
                    new_data.to_sql(selected_table, conn, if_exists="append", index=False)
                    st.success(f"成功导入 {len(new_data)} 条记录!")
                except Exception as e:
                    st.error(f"导入失败: {str(e)}")

                    