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

# Module/Script Name: 3_⚙️_系统设置.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day08 exexample Script.

import streamlit as st
import pandas  as pd

from utils.auth import check_permission

# 权限验证
if not st.session_state.auth.get("logged_in") or st.session_state.auth["role"] != "admin":
    st.error("无权限访问该页面")
    st.stop()

st.title("⚙️ 系统设置")

# 系统主题设置
with st.expander("主题配置", expanded=True):
    current_theme = st.session_state.get("theme", "light")
    new_theme = st.radio(
        "界面主题",
        ["light", "dark"],
        index=0 if current_theme == "light" else 1,
        horizontal=True
    )
    if new_theme != current_theme:
        st.session_state.theme = new_theme
        st.success(f"已切换至{new_theme}主题，请刷新页面生效")
    
    # 主题预览
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 亮色模式预览")
        st.image("https://i.imgur.com/3K6x7Hx.png")
    with col2:
        st.markdown("### 暗色模式预览")
        st.image("https://i.imgur.com/7V5D4Wz.png")

# 系统参数配置
with st.expander("高级配置"):
    log_level = st.selectbox(
        "日志级别",
        ["DEBUG", "INFO", "WARNING", "ERROR"],
        index=1
    )
    cache_time = st.slider("缓存时间（小时）", 1, 24, 6)
    if st.button("保存配置"):
        st.session_state.log_level = log_level
        st.session_state.cache_time = cache_time
        st.toast("配置已保存!", icon="✅")

# 系统信息
with st.expander("系统状态"):
    st.markdown(f"""
    - **当前版本**: v1.2.0
    - **运行时间**: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")}
    - **日志级别**: {st.session_state.get("log_level", "INFO")}
    - **用户数量**: {len(st.session_state.get("users", []))}
    """)

st.divider()
if st.button("返回主页"):
    st.switch_page("main_page.py")




