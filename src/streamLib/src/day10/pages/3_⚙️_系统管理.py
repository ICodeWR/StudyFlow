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

# Module/Script Name: 3_⚙️_系统管理.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
import os
from utils.database import get_connection, query_db
from utils.user import register_user

st.title("⚙️ 系统管理")

if st.session_state.auth["role"] != "admin":
    st.error("您没有访问此页面的权限")
    st.stop()

tab1, tab2, tab3 = st.tabs(["用户管理", "系统配置", "数据库维护"])

with tab1:
    st.subheader("用户账户管理")
    
    # 显示现有用户
    users = st.cache_data(ttl=60)(query_db)("SELECT username, role, created_at FROM users")
    st.dataframe(users, use_container_width=True)
    
    # 添加新用户
    with st.expander("添加新用户"):
        with st.form("user_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            role = st.selectbox("角色", ["admin", "editor", "viewer"])
            
            if st.form_submit_button("创建用户"):
                try:
                    register_user(username, password, role)
                    st.success(f"用户 {username} 创建成功!")
                    st.cache_data.clear()
                except Exception as e:
                    st.error(f"创建失败: {str(e)}")

with tab2:
    st.subheader("系统配置")
    
    # 主题配置
    st.write("### 主题设置")
    current_theme = st.selectbox("选择主题", ["light", "dark"], index=1)
    
    # 性能配置
    st.write("### 性能设置")
    cache_ttl = st.slider("缓存时间(秒)", 60, 3600, 300)
    
    if st.button("保存配置"):
        # 这里应该写入配置文件
        st.success("配置已保存 (示例: 实际需要写入配置文件)")

with tab3:
    st.subheader("数据库维护")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 备份数据库")
        if st.button("创建备份"):
            conn = get_connection()
            try:
                with open('data_backup.db', 'wb') as f:
                    for line in conn.iterdump():
                        f.write(f'{line}\n'.encode('utf-8'))
                st.success("备份创建成功!")
            except Exception as e:
                st.error(f"备份失败: {str(e)}")
    
    with col2:
        st.write("### 恢复数据库")
        backup_file = st.file_uploader("上传备份文件", type=["db"])
        if backup_file and st.button("恢复数据库"):
            try:
                with open('data.db', 'wb') as f:
                    f.write(backup_file.getvalue())
                st.success("数据库恢复成功!")
                st.cache_data.clear()
                st.cache_resource.clear()
            except Exception as e:
                st.error(f"恢复失败: {str(e)}")
    
    st.write("### 数据库状态")
    db_size = os.path.getsize('data.db') / (1024 * 1024)
    st.metric("数据库大小", f"{db_size:.2f} MB")
    
    if st.button("优化数据库"):
        conn = get_connection()
        try:
            conn.execute("VACUUM")
            st.success("数据库优化完成!")
        except Exception as e:
            st.error(f"优化失败: {str(e)}")

            