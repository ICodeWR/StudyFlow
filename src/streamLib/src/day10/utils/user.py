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

# Module/Script Name: user.py
# Author: ICodeWR (微信公众号同名）
# Created: 2025-03
# Description: streamlit day10 exexample Script.

import streamlit as st
from utils.database import get_connection
from utils.security import hash_password, verify_password


def authenticate():
    """用户认证"""
    with st.container():
        st.title("企业数据平台登录")
        
        cols = st.columns([1, 3, 1])
        with cols[1]:
            with st.form("login_form"):
                username = st.text_input("用户名")
                password = st.text_input("密码", type="password")
                remember = st.checkbox("记住我")
                
                if st.form_submit_button("登录"):
                    user = verify_credentials(username, password)
                    if user:
                        st.session_state.auth = {
                            "logged_in": True,
                            "user": user["username"],
                            "role": user["role"]
                        }
                        st.rerun()
                    else:
                        st.error("用户名或密码错误")

def verify_credentials(username, password):
    """验证用户凭证"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT username, password, role FROM users 
    WHERE username = ? AND status = 'active'
    """, (username,))
    
    user = cursor.fetchone()
    if user and verify_password(password, user["password"]):
        return dict(user)
    return None

def register_user(username, password, role="viewer"):
    """注册新用户"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 检查用户名是否存在
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        raise ValueError("用户名已存在")
    
    # 创建用户
    hashed_pw = hash_password(password)
    cursor.execute("""
    INSERT INTO users (username, password, role)
    VALUES (?, ?, ?)
    """, (username, hashed_pw, role))
    
    conn.commit()

def get_user_role(username):
    """获取用户角色"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result["role"] if result else "guest"

