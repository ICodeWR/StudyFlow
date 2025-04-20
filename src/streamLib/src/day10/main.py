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

# Module/Script Name: main.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
from utils.user import authenticate

# 初始化会话状态
if "auth" not in st.session_state:
    st.session_state.auth = {
        "logged_in": False,
        "user": None,
        "role": "guest"
    }

# 登录验证
if not st.session_state.auth["logged_in"]:
    authenticate()
    st.stop()

# 主界面配置
st.set_page_config(
    page_title="企业数据平台",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 显示登录信息
st.sidebar.success(f"欢迎, {st.session_state.auth['user']} ({st.session_state.auth['role']})")

# 导航菜单
pages = {
    "📈 数据仪表盘": "pages/1_📈_仪表盘.py",
    "🗃️ 数据管理": "pages/2_🗃️_数据管理.py",
    "⚙️ 系统管理": "pages/3_⚙️_系统管理.py"
}

# 只有管理员能看到系统管理
if st.session_state.auth["role"] != "admin":
    del pages["⚙️ 系统管理"]

selected = st.sidebar.selectbox("导航", list(pages.keys()))
st.switch_page(pages[selected])
