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

# Module/Script Name: main_page.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day08 exexample Script.

import streamlit as st
import pandas  as pd

from utils.auth import check_login

# 初始化会话状态
if "auth" not in st.session_state:
    st.session_state.auth = {"logged_in": False, "role": "guest"}

# 登录验证
def login():
    if st.session_state.auth["logged_in"]:
        return True
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("登录"):
                username = st.text_input("用户名")
                password = st.text_input("密码", type="password")
                if st.form_submit_button("登录"):
                    if check_login(username, password):
                        st.session_state.auth = {
                            "logged_in": True,
                            "role": "admin"  # 实际应从数据库获取角色
                        }
                        st.rerun()
                    else:
                        st.error("认证失败")
            return False

# 主界面布局
def main_layout():

    st.set_page_config(
        page_title="企业仪表盘",
        page_icon="🏢",
        layout="wide"
    )
    
    # 角色权限控制
    if st.session_state.auth["role"] == "admin":
        menu = ["主页", "数据分析", "用户管理", "系统设置"]
    else:
        menu = ["主页", "数据分析"]
    
    # 顶部导航栏
    with st.container():
        cols = st.columns([1,3,1])
        with cols[1]:
            selected = st.selectbox("导航", menu, label_visibility="collapsed")
    
    # 页面路由
    if selected == "主页":
        show_home()
    elif selected == "数据分析":
        st.switch_page("pages/1_📊_数据分析.py")
    elif selected == "用户管理":
        st.switch_page("pages/2_👥_用户管理.py")
    elif selected == "系统设置":
        st.switch_page("pages/3_⚙️_系统设置.py")

# 主页内容
def show_home():
    with st.container():
        st.title("企业数据驾驶舱")
        
        # 关键指标看板
        cols = st.columns(4)
        metrics = {
            "销售额": "¥1,234万",
            "同比增长": "+12.3%",
            "用户数": "8,888",
            "完成率": "89%"
        }
        for col, (k, v) in zip(cols, metrics.items()):
            col.metric(k, v)
        
        # 主图表区
        tab1, tab2 = st.tabs(["趋势分析", "地域分布"])
        with tab1:
            st.line_chart({"数据": [1,3,2,4,3,5]})
        with tab2:
            st.map(pd.DataFrame({
                "lat": [31.2304, 39.9042, 23.1291],
                "lon": [121.4737, 116.4074, 113.2644],
                "city": ["上海", "北京", "广州"]
            }))

# 程序入口
if not login():
    st.stop()

main_layout()