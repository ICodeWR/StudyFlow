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

# Module/Script Name: 2_👥_用户管理.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day08 exexample Script.


import streamlit as st
import pandas as pd
from utils.auth import check_permission

# 权限验证
if not st.session_state.auth.get("logged_in") or st.session_state.auth["role"] != "admin":
    st.error("无权限访问该页面")
    st.stop()

st.title("👥 用户管理系统")

# 初始化用户数据（示例数据）
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame({
        "用户名": ["admin", "user1"],
        "角色": ["admin", "user"],
        "创建时间": ["2024-01-01", "2024-01-02"]
    })

# 双列布局
col_list, col_form = st.columns([2, 3])

with col_list:
    st.subheader("用户列表")
    st.dataframe(
        st.session_state.users,
        use_container_width=True,
        hide_index=True
    )

with col_form:
    st.subheader("用户操作")
    tab_add, tab_edit = st.tabs(["新增用户", "编辑用户"])
    
    # 新增用户表单
    with tab_add:
        with st.form("add_user"):
            new_user = st.text_input("用户名", key="new_user")
            new_role = st.selectbox("角色", ["admin", "user"], key="new_role")
            if st.form_submit_button("创建用户"):
                if new_user in st.session_state.users["用户名"].values:
                    st.error("用户名已存在")
                else:
                    new_data = pd.DataFrame([{
                        "用户名": new_user,
                        "角色": new_role,
                        "创建时间": pd.Timestamp.now().strftime("%Y-%m-%d")
                    }])
                    st.session_state.users = pd.concat([st.session_state.users, new_data])
                    st.rerun()
    
    # 编辑用户表单
    with tab_edit:
        selected_user = st.selectbox(
            "选择用户",
            st.session_state.users["用户名"],
            key="edit_user"
        )
        user_data = st.session_state.users[
            st.session_state.users["用户名"] == selected_user
        ].iloc[0]
        
        with st.form("edit_user_form"):
            edit_role = st.selectbox(
                "角色",
                ["admin", "user"],
                index=0 if user_data["角色"] == "admin" else 1,
                key="edit_role"
            )
            if st.form_submit_button("更新信息"):
                st.session_state.users.loc[
                    st.session_state.users["用户名"] == selected_user, "角色"
                ] = edit_role
                st.rerun()
        
        if st.button("删除用户", type="primary"):
            st.session_state.users = st.session_state.users[
                st.session_state.users["用户名"] != selected_user
            ]
            st.rerun()

st.divider()
if st.button("返回主页"):
    st.switch_page("main_page.py")




